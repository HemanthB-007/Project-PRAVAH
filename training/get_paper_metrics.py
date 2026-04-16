import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, average_precision_score
import xgboost as xgb
from imblearn.over_sampling import SMOTE

# 1. Load Data
df = pd.read_csv("datasets/processed/pravah_master_dataset.csv")
X = df[[
    "rainfall_mm", "rainfall_3day_avg", "rainfall_7day_avg", 
    "mean_elevation", "drainage_density", "vegetation_density"
]]
y = df["flood_event"]

# 2. Multicollinearity / Feature Correlation
print("--- FEATURE CORRELATION ---")
print(X[["rainfall_mm", "rainfall_3day_avg", "rainfall_7day_avg"]].corr())

# 3. AUC Scores
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
smote = SMOTE(random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

# Train XGBoost
xgb_model = xgb.XGBClassifier(n_estimators=200, max_depth=5, learning_rate=0.05)
xgb_model.fit(X_train_res, y_train_res)

# Predict Probabilities
y_probs = xgb_model.predict_proba(X_test)[:, 1]

print("\n--- AUC SCORES ---")
print(f"ROC-AUC Score: {roc_auc_score(y_test, y_probs):.4f}")
print(f"PR-AUC (Average Precision): {average_precision_score(y_test, y_probs):.4f}")