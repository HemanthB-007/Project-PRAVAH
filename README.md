# Project PRAVAH

**AI-Driven Urban Flood Early Warning System**

## Overview
PRAVAH is a machine learning pipeline and real-time dashboard built to predict urban flooding. It combines weather data, elevation maps, and drainage network data to calculate flood risks and provide early warnings.

## Key Features
* **Flood Prediction Model:** Uses XGBoost to predict flood risks based on rainfall and terrain data.
* **Real-Time Dashboard:** An interactive Leaflet.js map that displays risk levels for specific city zones.
* **Low-Latency Backend:** Powered by FastAPI for quick data processing and predictions.
* **Actionable Alerts:** Automatically suggests response protocols based on Low, Moderate, or High risk levels.

## Project Structure
* `backend/`: FastAPI application endpoints and caching.
* `dashboard/`: Leaflet.js UI, styles, and frontend visualization.
* `datasets/`: Scripts to prepare and process rainfall, elevation, drainage, and vegetation data.
* `models/`: Trained machine learning models.
* `training/`: Feature engineering, model training, and evaluation scripts.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone [https://github.com/HemanthB-007/Project-PRAVAH.git](https://github.com/HemanthB-007/Project-PRAVAH.git)
   cd Project-PRAVAH

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Authors
* Hemanth Boddupally
* Gautam Kumar
* Parampreet Kaur
* Maddula P V N Sai Sri Akshay
* Hema Sri
