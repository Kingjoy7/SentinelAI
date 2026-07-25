"""
event_generator.py

Generates realistic normal cybersecurity events
from employee profiles.
"""

from pathlib import Path
import random
from datetime import datetime, timedelta

import pandas as pd

from schema import (
    DEPARTMENT_RESOURCES,
    DEVICE_TYPES,
    BROWSERS,
    RANDOM_SEED,
    MIN_SESSION_DURATION,
    MAX_SESSION_DURATION,
)

random.seed(RANDOM_SEED)

# ------------------------
# Paths
# ------------------------

CURRENT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = CURRENT_DIR.parent
DATASET_DIR = BACKEND_DIR / "datasets"

PROFILE_FILE = DATASET_DIR / "user_profiles.csv"
OUTPUT_FILE = DATASET_DIR / "normal_events.csv"

# ------------------------
# Helper Functions
# ------------------------

def random_timestamp(base_date, preferred_hour):

    day_offset = random.randint(0, 30)

    hour = max(
        0,
        min(
            23,
            preferred_hour + random.randint(-1, 1)
        )
    )

    minute = random.randint(0, 59)

    second = random.randint(0, 59)

    return base_date + timedelta(
        days=day_offset,
        hours=hour,
        minutes=minute,
        seconds=second
    )


def choose_resource(profile):

    department = profile["department"]

    preferred = profile["preferred_resource"]

    if random.random() < 0.80:
        return preferred

    pool = DEPARTMENT_RESOURCES[department]

    return random.choice(pool)


# ------------------------
# Main Generator
# ------------------------

def generate_normal_events(events_per_user=100):

    profiles = pd.read_csv(PROFILE_FILE)

    base_date = datetime.now() - timedelta(days=30)

    rows = []

    for _, profile in profiles.iterrows():

        for _ in range(events_per_user):

            browser = (
                profile["preferred_browser"]
                if random.random() < 0.95
                else random.choice(BROWSERS)
            )

            device = (
                profile["preferred_device"]
                if random.random() < 0.95
                else random.choice(DEVICE_TYPES)
            )

            timestamp = random_timestamp(
                base_date,
                int(profile["preferred_login_hour"])
            )

            failed_attempts = (
                0
                if random.random() < 0.95
                else random.randint(1, 2)
            )

            session_duration = random.randint(
                MIN_SESSION_DURATION,
                MAX_SESSION_DURATION
            )

            command_count = random.randint(5, 40)

            rows.append({

                "timestamp": timestamp,

                "user_id": profile["user_id"],

                "user_role": profile["user_role"],

                "department": profile["department"],

                "country": profile["home_country"],

                "city": profile["home_city"],

                "device_type": device,

                "device_fingerprint":
                    profile["device_fingerprint"],

                "browser": browser,

                "os":
                    profile["operating_system"],

                "auth_method":
                    profile["preferred_auth_method"],

                "resource_accessed":
                    choose_resource(profile),

                "login_hour":
                    timestamp.hour,

                "session_duration":
                    session_duration,

                "failed_login_attempts":
                    failed_attempts,

                "command_count":
                    command_count,

                "attack_type":
                    "Normal",

                "is_anomaly":
                    0

            })

    df = pd.DataFrame(rows)

    df.to_csv(OUTPUT_FILE, index=False)

    print("=" * 60)
    print(f"Generated {len(df)} Normal Events")
    print(f"Saved to {OUTPUT_FILE}")
    print("=" * 60)

    return df


if __name__ == "__main__":

    generate_normal_events(events_per_user=100)