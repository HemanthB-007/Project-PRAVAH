import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE
import xgboost as xgb
import joblib

# ------------------------
# Load dataset
# ------------------------
df = pd.read_csv("datasets/processed/pravah_master_dataset.csv")

# Target
y = df["flood_event"]

# Features
X = df[[
    "rainfall_mm",
    "rainfall_3day_avg",
    "rainfall_7day_avg",
    "mean_elevation",
    "drainage_density",
    "vegetation_density"
]]

# ------------------------
# Check class distribution
# ------------------------
print("Class Distribution:")
print(y.value_counts())

# ------------------------
# Train-Test Split (STRATIFIED)
# ------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ------------------------
# Handle Imbalance (SMOTE)
# ------------------------
smote = SMOTE(random_state=42)
X_train, y_train = smote.fit_resample(X_train, y_train)

# ------------------------
# Random Forest (for comparison)
# ------------------------
rf = RandomForestClassifier(
    n_estimators=200,
    class_weight="balanced",
    random_state=42
)

rf.fit(X_train, y_train)
rf_preds = rf.predict(X_test)

print("\n===== Random Forest Results =====")
print(confusion_matrix(y_test, rf_preds))
print(classification_report(y_test, rf_preds))


# ------------------------
# XGBoost Model (MAIN MODEL)
# ------------------------
xgb_model = xgb.XGBClassifier(
    n_estimators=200,
    max_depth=5,
    learning_rate=0.05,
    random_state=42,
    use_label_encoder=False,
    eval_metric="logloss"
)

xgb_model.fit(X_train, y_train)

# ------------------------
# 🔥 IMPORTANT: Use probabilities + custom threshold
# ------------------------
probs = xgb_model.predict_proba(X_test)[:, 1]

threshold = 0.3  # 👈 KEY FIX

xgb_preds = (probs > threshold).astype(int)

# ------------------------
# Evaluation
# ------------------------
print("\n===== XGBoost Results (Threshold = 0.3) =====")
print(confusion_matrix(y_test, xgb_preds))
print(classification_report(y_test, xgb_preds))

# ------------------------
# Probability Insights
# ------------------------
print("\nProbability Stats:")
print("Min:", probs.min())
print("Max:", probs.max())
print("Mean:", probs.mean())

print("\nSample Probabilities:", probs[:10])

# ------------------------
# Save Model
# ------------------------
joblib.dump(xgb_model, "models/flood_prediction_model.pkl")

print("\n✅ Model saved successfully")