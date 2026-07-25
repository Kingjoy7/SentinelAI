from pathlib import Path
import joblib
import pandas as pd

from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, confusion_matrix


# ======================================================
# Paths
# ======================================================

CURRENT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = CURRENT_DIR.parent

DATASET_DIR = BACKEND_DIR / "datasets"
MODEL_DIR = BACKEND_DIR / "trained_models"

X_FILE = DATASET_DIR / "X.csv"
Y_FILE = DATASET_DIR / "y_binary.csv"

MODEL_FILE = MODEL_DIR / "isolation_forest.pkl"


# ======================================================
# Load Data
# ======================================================

print("Loading data...")

X = pd.read_csv(X_FILE)
y = pd.read_csv(Y_FILE).squeeze()

print(f"Samples : {len(X)}")
print(f"Features: {X.shape[1]}")


# ======================================================
# Estimate contamination
# ======================================================

contamination = y.mean()

print(f"Estimated anomaly ratio: {contamination:.4f}")


# ======================================================
# Train Isolation Forest
# ======================================================

print("\nTraining Isolation Forest...\n")

model = IsolationForest(
    n_estimators=200,
    contamination=contamination,
    random_state=42,
    n_jobs=-1
)

model.fit(X)


# ======================================================
# Predict
# ======================================================

pred = model.predict(X)

# IsolationForest:
# -1 = anomaly
#  1 = normal

pred = [1 if x == -1 else 0 for x in pred]


# ======================================================
# Evaluation
# ======================================================

print("=" * 60)
print("CONFUSION MATRIX")
print("=" * 60)

print(confusion_matrix(y, pred))

print("\n")

print("=" * 60)
print("CLASSIFICATION REPORT")
print("=" * 60)

print(classification_report(y, pred))


# ======================================================
# Save model
# ======================================================

joblib.dump(model, MODEL_FILE)

print("\nModel saved successfully!")

print(MODEL_FILE)