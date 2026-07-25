"""
user_profiles.py

Generates stable employee profiles for SentinelAI.
Each employee keeps the same baseline behaviour throughout the simulation.
"""

from pathlib import Path
import random

import pandas as pd
from faker import Faker

from schema import (
    USER_ROLES,
    ROLE_TO_DEPARTMENT,
    COUNTRY_CITY_MAP,
    DEVICE_TYPES,
    BROWSERS,
    OPERATING_SYSTEMS,
    AUTH_METHODS,
    DEPARTMENT_RESOURCES,
    RANDOM_SEED,
)

# -----------------------------
# Paths
# -----------------------------

CURRENT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = CURRENT_DIR.parent
DATASET_DIR = BACKEND_DIR / "datasets"

DATASET_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = DATASET_DIR / "user_profiles.csv"

# -----------------------------
# Faker
# -----------------------------

fake = Faker()
fake.seed_instance(RANDOM_SEED)
random.seed(RANDOM_SEED)


# -----------------------------
# Helper Functions
# -----------------------------

def generate_user_id(index: int) -> str:
    return f"EMP{index:04d}"


def choose_country_city():
    country = random.choice(list(COUNTRY_CITY_MAP.keys()))
    city = random.choice(COUNTRY_CITY_MAP[country])
    return country, city


def create_device_fingerprint(user_id: str):
    return f"{user_id}-{fake.uuid4()[:8]}"


def preferred_login_hour(role):
    if role == "Engineer":
        return random.randint(8, 10)

    if role == "HR":
        return random.randint(9, 10)

    if role == "Finance":
        return random.randint(8, 9)

    if role == "Admin":
        return random.randint(7, 9)

    return random.randint(8, 10)


# -----------------------------
# Main Function
# -----------------------------

def generate_user_profiles(num_users=500):

    profiles = []

    for i in range(1, num_users + 1):

        role = random.choice(USER_ROLES)

        department = ROLE_TO_DEPARTMENT[role]

        country, city = choose_country_city()

        preferred_device = random.choice(DEVICE_TYPES)

        preferred_browser = random.choice(BROWSERS)

        operating_system = random.choice(OPERATING_SYSTEMS)

        auth_method = random.choice(AUTH_METHODS)

        preferred_resource = random.choice(
            DEPARTMENT_RESOURCES[department]
        )

        profile = {

            "user_id": generate_user_id(i),

            "user_role": role,

            "department": department,

            "home_country": country,

            "home_city": city,

            "preferred_device": preferred_device,

            "preferred_browser": preferred_browser,

            "operating_system": operating_system,

            "preferred_auth_method": auth_method,

            "preferred_login_hour": preferred_login_hour(role),

            "preferred_resource": preferred_resource,

            "device_fingerprint": create_device_fingerprint(
                generate_user_id(i)
            ),
        }

        profiles.append(profile)

    df = pd.DataFrame(profiles)

    df.to_csv(OUTPUT_FILE, index=False)

    print("=" * 50)
    print(f"Generated {len(df)} Employee Profiles")
    print(f"Saved to : {OUTPUT_FILE}")
    print("=" * 50)

    return df


# -----------------------------
# Run File
# -----------------------------

if __name__ == "__main__":

    generate_user_profiles(500)