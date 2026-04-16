import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
import joblib
from sklearn.model_selection import train_test_split

# FIX 1: Added ../ to go up one folder
df = pd.read_csv("../datasets/processed/pravah_master_dataset.csv")

y = df["flood_event"]
X = df[[
    "rainfall_mm",
    "rainfall_3day_avg",
    "rainfall_7day_avg",
    "mean_elevation",
    "drainage_density",
    "vegetation_density"
]]

# MUST match the split used in train_flood_model.py
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# FIX 2: Added ../ to go up one folder
model = joblib.load("../models/flood_prediction_model.pkl")

# Apply the 0.25 threshold to the test set
probs = model.predict_proba(X_test)[:, 1]
y_pred = (probs > 0.25).astype(int)

cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, cmap="Blues", fmt="d")
plt.title("Flood Prediction Confusion Matrix (Threshold = 0.25)")
plt.xlabel("Predicted")
plt.ylabel("Actual")

# FIX 3: Saving as fig2.png directly in the training folder in high-res!
plt.savefig("../dashboard/confusion_matrix.png", dpi=300, bbox_inches='tight')
print("✅ Success! confusion_matrix.png has been generated in your training folder.")