import pandas as pd
import shap
import xgboost as xgb
import joblib
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

# FIX 1: Added ../ to go up one folder to the Pravah root
df = pd.read_csv("../datasets/processed/pravah_master_dataset.csv")

X = df[[
    "rainfall_mm",
    "rainfall_3day_avg",
    "rainfall_7day_avg",
    "mean_elevation",
    "drainage_density",
    "vegetation_density"
]]

y = df["flood_event"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# FIX 2: Added ../ here as well!
model = joblib.load("../models/flood_prediction_model.pkl")

print("Generating SHAP values (this might take a few seconds)...")
explainer = shap.Explainer(model)
shap_values = explainer(X_test)

plt.figure(figsize=(8, 5))
shap.plots.bar(shap_values, show=False)

# This will save fig3.png directly into your current 'training' folder
plt.savefig("../dashboard/shap_feature_importance.png", dpi=300, bbox_inches='tight')