from pathlib import Path
import joblib
import pandas as pd

from sklearn.preprocessing import LabelEncoder


# =====================================================
# Paths
# =====================================================

CURRENT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = CURRENT_DIR.parent

DATASET_DIR = BACKEND_DIR / "datasets"
MODEL_DIR = BACKEND_DIR / "trained_models"

MODEL_DIR.mkdir(exist_ok=True)

INPUT_FILE = DATASET_DIR / "final_dataset.csv"

X_FILE = DATASET_DIR / "X.csv"
Y_BINARY_FILE = DATASET_DIR / "y_binary.csv"
Y_MULTI_FILE = DATASET_DIR / "y_multiclass.csv"

ENCODER_FILE = MODEL_DIR / "encoders.pkl"


# =====================================================
# Load Dataset
# =====================================================

print("Loading dataset...")

df = pd.read_csv(INPUT_FILE)

print(f"Dataset Shape : {df.shape}")


# =====================================================
# Drop columns not useful for ML
# =====================================================

drop_columns = [
    "timestamp",
    "user_id",
]

for col in drop_columns:
    if col in df.columns:
        df.drop(columns=col, inplace=True)


# =====================================================
# Binary Label
# =====================================================

y_binary = df["is_anomaly"]


# =====================================================
# Multi-class Label
# =====================================================

y_multi = df["attack_type"]


# =====================================================
# Remove target columns
# =====================================================

X = df.drop(
    columns=[
        "attack_type",
        "is_anomaly",
    ]
)


# =====================================================
# Encode categorical features
# =====================================================

encoders = {}

categorical_columns = X.select_dtypes(include="object").columns

print("\nEncoding categorical columns...")

for col in categorical_columns:

    encoder = LabelEncoder()

    X[col] = encoder.fit_transform(X[col].astype(str))

    encoders[col] = encoder

    print(f"Encoded -> {col}")


# =====================================================
# Save processed data
# =====================================================

X.to_csv(X_FILE, index=False)

y_binary.to_csv(Y_BINARY_FILE, index=False)

y_multi.to_csv(Y_MULTI_FILE, index=False)

joblib.dump(encoders, ENCODER_FILE)


print("\n========================================")
print("Feature Engineering Complete")
print("========================================")

print(f"Features Shape : {X.shape}")
print(f"Binary Labels  : {y_binary.shape}")
print(f"Multi Labels   : {y_multi.shape}")

print("\nFiles Saved:")

print(X_FILE)
print(Y_BINARY_FILE)
print(Y_MULTI_FILE)
print(ENCODER_FILE)