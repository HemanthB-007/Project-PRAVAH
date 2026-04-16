from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import joblib
import os

app = FastAPI(title="PRAVAH Command Center API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 1. Load Model and Lookup Table on Startup ---
# Set up absolute paths so it doesn't matter where you run the server from
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "../models/flood_prediction_model.pkl")
LOOKUP_PATH = os.path.join(BASE_DIR, "../datasets/processed/zone_features_lookup.csv")

model = joblib.load(MODEL_PATH)
zone_df = pd.read_csv(LOOKUP_PATH)

@app.post("/predict")
async def predict_flood(rainfall_mm: float, rainfall_3day_avg: float, rainfall_7day_avg: float):
    
    # --- 2. Vectorized Feature Engineering ---
    inference_df = zone_df.copy()
    inference_df['rainfall_mm'] = rainfall_mm
    inference_df['rainfall_3day_avg'] = rainfall_3day_avg
    inference_df['rainfall_7day_avg'] = rainfall_7day_avg
    
    feature_cols = [
        'rainfall_mm', 'rainfall_3day_avg', 'rainfall_7day_avg', 
        'mean_elevation', 'drainage_density', 'vegetation_density'
    ]
    
    X_predict = inference_df[feature_cols]
    
    # --- 3. Run Inference on all 227 zones instantly ---
    probabilities = model.predict_proba(X_predict)[:, 1]
    
    # --- 4. Apply Safety Logic with Dynamic Rain Factor ---
    zone_results = {}
    max_modified_prob = 0.0  
    
    for i, base_prob in enumerate(probabilities):
        elevation = float(inference_df.iloc[i]['mean_elevation'])
        
        rain_factor = min(1.0, rainfall_mm / 50.0) 
        modifier = (8.0 - elevation) * 0.06 * rain_factor 
        final_prob = float(base_prob) + modifier
        final_prob = max(0.0, min(1.0, final_prob))
        
        if final_prob > max_modified_prob:
            max_modified_prob = final_prob
            
        if final_prob > 0.25:
            risk = "HIGH"
        elif final_prob > 0.10:
            risk = "MODERATE"
        else:
            risk = "LOW"
            
        zone_id = str(inference_df.iloc[i]['zone_id'])
        zone_results[zone_id] = {
            "name": inference_df.iloc[i]['zone_name'],
            "probability": final_prob, 
            "risk_level": risk
        }

    # --- 5. Sync the Main Dashboard Gauge ---
    if max_modified_prob > 0.25:
        overall_risk = "HIGH"
    elif max_modified_prob > 0.10:
        overall_risk = "MODERATE"
    else:
        overall_risk = "LOW"

    return {
        "risk_level": overall_risk,
        "flood_probability": max_modified_prob, 
        "zone_predictions": zone_results
    }