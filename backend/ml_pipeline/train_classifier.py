from pathlib import Path
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import LabelEncoder


# ======================================================
# Paths
# ======================================================

CURRENT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = CURRENT_DIR.parent

DATASET_DIR = BACKEND_DIR / "datasets"
MODEL_DIR = BACKEND_DIR / "trained_models"

X_FILE = DATASET_DIR / "X.csv"
Y_FILE = DATASET_DIR / "y_multiclass.csv"

MODEL_FILE = MODEL_DIR / "random_forest.pkl"
LABEL_ENCODER_FILE = MODEL_DIR / "attack_label_encoder.pkl"


# ======================================================
# Load Data
# ======================================================

print("Loading dataset...")

X = pd.read_csv(X_FILE)
y = pd.read_csv(Y_FILE).squeeze()

print(f"Samples : {len(X)}")
print(f"Features: {X.shape[1]}")


# ======================================================
# Encode Labels
# ======================================================

label_encoder = LabelEncoder()

y = label_encoder.fit_transform(y)

joblib.dump(label_encoder, LABEL_ENCODER_FILE)


# ======================================================
# Train/Test Split
# ======================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print(f"\nTraining Samples : {len(X_train)}")
print(f"Testing Samples  : {len(X_test)}")


# ======================================================
# Train Random Forest
# ======================================================

print("\nTraining Random Forest...\n")

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)


# ======================================================
# Prediction
# ======================================================

pred = model.predict(X_test)


# ======================================================
# Evaluation
# ======================================================

print("=" * 60)
print("Accuracy")
print("=" * 60)

print(f"{accuracy_score(y_test, pred):.4f}")

print("\n")

print("=" * 60)
print("Confusion Matrix")
print("=" * 60)

print(confusion_matrix(y_test, pred))

print("\n")

print("=" * 60)
print("Classification Report")
print("=" * 60)

print(classification_report(
    y_test,
    pred,
    target_names=label_encoder.classes_
))


# ======================================================
# Top Features
# ======================================================

importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

print("\n")

print("=" * 60)
print("Top 10 Important Features")
print("=" * 60)

print(importance.head(10))


# ======================================================
# Save Model
# ======================================================

joblib.dump(model, MODEL_FILE)

print("\nRandom Forest saved successfully!")

print(MODEL_FILE)