import joblib
import pandas as pd
from pathlib import Path

# ==========================================================
# Paths
# ==========================================================

CURRENT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = CURRENT_DIR.parent

MODEL_DIR = BACKEND_DIR / "trained_models"
DATASET_DIR = BACKEND_DIR / "datasets"

RF_MODEL = MODEL_DIR / "random_forest.pkl"
ENCODER_FILE = MODEL_DIR / "attack_label_encoder.pkl"

DATA_FILE = DATASET_DIR / "final_dataset.csv"


# ==========================================================
# Load Model
# ==========================================================

model = joblib.load(RF_MODEL)
label_encoder = joblib.load(ENCODER_FILE)

df = pd.read_csv(DATA_FILE)


# ==========================================================
# Rule Based Explanations
# ==========================================================

def generate_explanation(row):

    attack = row["Predicted Attack"]

    reasons = []
    actions = []
    severity = "Low"

    if attack == "Brute Force":

        severity = "High"

        reasons = [
            "Multiple failed login attempts detected.",
            "Very short session duration.",
            "Repeated authentication failures."
        ]

        actions = [
            "Temporarily lock the account.",
            "Require Multi-Factor Authentication.",
            "Notify SOC analyst."
        ]


    elif attack == "Credential Stuffing":

        severity = "High"

        reasons = [
            "Multiple credential validation attempts.",
            "Suspicious authentication behaviour.",
            "Abnormal login success/failure pattern."
        ]

        actions = [
            "Reset user password.",
            "Monitor future login attempts.",
            "Enable MFA."
        ]


    elif attack == "Device Spoofing":

        severity = "High"

        reasons = [
            "Unknown device detected.",
            "Device fingerprint mismatch.",
            "Browser/OS differs from normal profile."
        ]

        actions = [
            "Terminate active session.",
            "Verify device ownership.",
            "Request identity verification."
        ]


    elif attack == "Impossible Travel":

        severity = "Medium"

        reasons = [
            "Login location changed drastically.",
            "Travel between locations is unrealistic.",
            "User behaviour differs from historical pattern."
        ]

        actions = [
            "Verify login with user.",
            "Check VPN usage.",
            "Require MFA."
        ]


    elif attack == "Insider Threat":

        severity = "Critical"

        reasons = [
            "Abnormally high command execution.",
            "Sensitive resource accessed.",
            "Long suspicious session."
        ]

        actions = [
            "Disable account immediately.",
            "Notify Incident Response Team.",
            "Begin forensic investigation."
        ]


    elif attack == "Lateral Movement":

        severity = "Critical"

        reasons = [
            "Multiple internal resources accessed.",
            "Suspicious movement across systems.",
            "Possible privilege escalation."
        ]

        actions = [
            "Isolate affected machine.",
            "Block internal communication.",
            "Start incident investigation."
        ]


    else:

        severity = "Safe"

        reasons = [
            "User behaviour matches baseline profile."
        ]

        actions = [
            "No action required."
        ]


    return severity, reasons, actions


# ==========================================================
# Prepare Features
# ==========================================================

X = pd.read_csv(DATASET_DIR / "X.csv")

pred = model.predict(X)

pred = label_encoder.inverse_transform(pred)

df["Predicted Attack"] = pred


# ==========================================================
# Confidence
# ==========================================================

prob = model.predict_proba(X)

confidence = prob.max(axis=1) * 100

df["Confidence"] = confidence.round(2)


# ==========================================================
# Build Explanations
# ==========================================================

severity_list = []
reason_list = []
action_list = []

print("Generating explanations...\n")

for _, row in df.iterrows():

    sev, reason, action = generate_explanation(row)

    severity_list.append(sev)

    reason_list.append("\n".join(reason))

    action_list.append("\n".join(action))


df["Severity"] = severity_list
df["Reasons"] = reason_list
df["Recommended Actions"] = action_list


# ==========================================================
# Save
# ==========================================================

OUTPUT = DATASET_DIR / "predictions_with_explanations.csv"

df.to_csv(OUTPUT, index=False)

print("="*60)
print("Explainability Completed")
print("="*60)

print(df[[
    "Predicted Attack",
    "Confidence",
    "Severity"
]].head())

print()

print(f"Saved -> {OUTPUT}")