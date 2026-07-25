import random
from pathlib import Path

import numpy as np
import pandas as pd

from schema import (
    ATTACK_DISTRIBUTION,
    COUNTRY_CITY_MAP,
    DEVICE_TYPES,
    BROWSERS,
    OPERATING_SYSTEMS,
    RANDOM_SEED,
)

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

CURRENT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = CURRENT_DIR.parent
DATASET_DIR = BACKEND_DIR / "datasets"

INPUT_FILE = DATASET_DIR / "normal_events.csv"
OUTPUT_FILE = DATASET_DIR / "final_dataset.csv"


# -------------------------------------------------------
# Helper
# -------------------------------------------------------

def sample_rows(df, percent):
    count = max(1, int(len(df) * percent))
    return np.random.choice(df.index, count, replace=False)


# -------------------------------------------------------
# Brute Force
# -------------------------------------------------------

def inject_brute_force(df):

    idx = sample_rows(df, ATTACK_DISTRIBUTION["Brute Force"])

    df.loc[idx, "failed_login_attempts"] = np.random.randint(
        6,
        15,
        len(idx)
    )

    df.loc[idx, "session_duration"] = np.random.randint(
        1,
        5,
        len(idx)
    )

    df.loc[idx, "attack_type"] = "Brute Force"
    df.loc[idx, "is_anomaly"] = 1

    return df


# -------------------------------------------------------
# Impossible Travel
# -------------------------------------------------------

def inject_impossible_travel(df):

    idx = sample_rows(df, ATTACK_DISTRIBUTION["Impossible Travel"])

    countries = list(COUNTRY_CITY_MAP.keys())

    unusual_browsers = [
        "Tor Browser",
        "Brave",
        "Firefox"
    ]

    unusual_auth = [
        "Password",
        "OTP"
    ]

    for i in idx:

        # New Country
        current = df.at[i, "country"]

        possible = [c for c in countries if c != current]

        new_country = random.choice(possible)

        df.at[i, "country"] = new_country
        df.at[i, "city"] = random.choice(COUNTRY_CITY_MAP[new_country])

        # Login at an unusual hour
        df.at[i, "login_hour"] = random.choice(
            [0, 1, 2, 3, 4, 5]
        )

        # Different browser
        if "browser" in df.columns:
            df.at[i, "browser"] = random.choice(unusual_browsers)

        # Different device
        if "device" in df.columns:
            df.at[i, "device"] = random.choice(
                ["Laptop", "Mobile", "Tablet"]
            )

        # Different authentication
        if "authentication_method" in df.columns:
            df.at[i, "authentication_method"] = random.choice(unusual_auth)

        if "auth_method" in df.columns:
            df.at[i, "auth_method"] = random.choice(unusual_auth)

        # Slightly shorter session
        df.at[i, "session_duration"] = random.randint(5, 20)

        # Small number of failed attempts
        df.at[i, "failed_login_attempts"] = random.randint(1, 3)

        df.at[i, "attack_type"] = "Impossible Travel"
        df.at[i, "is_anomaly"] = 1

    return df


# -------------------------------------------------------
# Credential Stuffing
# -------------------------------------------------------

def inject_credential_stuffing(df):

    idx = sample_rows(df, ATTACK_DISTRIBUTION["Credential Stuffing"])

    df.loc[idx, "failed_login_attempts"] = np.random.randint(
        3,
        8,
        len(idx)
    )

    df.loc[idx, "session_duration"] = np.random.randint(
        3,
        10,
        len(idx)
    )

    df.loc[idx, "attack_type"] = "Credential Stuffing"
    df.loc[idx, "is_anomaly"] = 1

    return df


# -------------------------------------------------------
# Device Spoofing
# -------------------------------------------------------

def inject_device_spoofing(df):

    idx = sample_rows(df, ATTACK_DISTRIBUTION["Device Spoofing"])

    for i in idx:

        df.at[i, "device"] = random.choice(DEVICE_TYPES)
        df.at[i, "browser"] = random.choice(BROWSERS)
        df.at[i, "operating_system"] = random.choice(OPERATING_SYSTEMS)

        df.at[i, "device_fingerprint"] = (
            "SPOOF-"
            + str(random.randint(100000, 999999))
        )

        df.at[i, "attack_type"] = "Device Spoofing"
        df.at[i, "is_anomaly"] = 1

    return df


# -------------------------------------------------------
# Insider Threat
# -------------------------------------------------------

def inject_insider_threat(df):

    idx = sample_rows(df, ATTACK_DISTRIBUTION["Insider Threat"])

    sensitive_resources = [
        "Database",
        "Finance Portal",
        "Admin Console",
        "Payroll System",
    ]

    for i in idx:

        df.at[i, "resource"] = random.choice(sensitive_resources)

        df.at[i, "command_count"] = random.randint(
            150,
            400,
        )

        df.at[i, "session_duration"] = random.randint(
            120,
            300,
        )

        df.at[i, "attack_type"] = "Insider Threat"
        df.at[i, "is_anomaly"] = 1

    return df


# -------------------------------------------------------
# Lateral Movement
# -------------------------------------------------------

def inject_lateral_movement(df):

    idx = sample_rows(df, ATTACK_DISTRIBUTION["Lateral Movement"])

    for i in idx:

        df.at[i, "command_count"] = random.randint(
            80,
            200,
        )

        df.at[i, "resource"] = "Internal Server"

        df.at[i, "session_duration"] = random.randint(
            90,
            180,
        )

        df.at[i, "attack_type"] = "Lateral Movement"
        df.at[i, "is_anomaly"] = 1

    return df


# -------------------------------------------------------
# Pipeline
# -------------------------------------------------------

def inject_all_attacks():

    df = pd.read_csv(INPUT_FILE)

    df["attack_type"] = "Normal"
    df["is_anomaly"] = 0

    df = inject_brute_force(df)
    df = inject_impossible_travel(df)
    df = inject_credential_stuffing(df)
    df = inject_device_spoofing(df)
    df = inject_insider_threat(df)
    df = inject_lateral_movement(df)

    df = df.sample(frac=1, random_state=RANDOM_SEED).reset_index(drop=True)

    df.to_csv(OUTPUT_FILE, index=False)

    print("=" * 60)
    print("Attack Injection Complete")
    print("=" * 60)
    print(df["attack_type"].value_counts())
    print("=" * 60)
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    inject_all_attacks()