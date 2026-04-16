# PRAVAH
[cite_start]**Integrating Cost-Sensitive Machine Learning and Micro-Topography for Urban Flood Early Warning** [cite: 1, 3]

## Overview
[cite_start]PRAVAH is an end-to-end machine learning pipeline and real-time geospatial dashboard engineered to revolutionize flood risk assessment through a dual-engine architecture[cite: 10]. [cite_start]The system mitigates the escalating risk to public safety caused by urban flooding in coastal cities[cite: 8]. [cite_start]It addresses the complex non-linear relationship between sudden precipitation and antecedent soil moisture levels[cite: 8]. [cite_start]By shifting the operational focus from generalized accuracy to human-centric sensitivity, PRAVAH prevents catastrophic failures to predict rare, high-impact flood events[cite: 9, 13].

## Architecture & Methodology
* [cite_start]**Spatiotemporal Data Fusion**: The system fuses historical meteorological data with static structural topologies to generate cumulative moisture vectors representing soil saturation[cite: 11]. [cite_start]It utilizes mean elevation and drainage density sourced from OpenStreetMap and USGS Digital Elevation Models[cite: 11]. 
* [cite_start]**Class Imbalance Resolution**: Historical disaster datasets suffer from severe class imbalance, specifically a 1:71 ratio in this regional dataset[cite: 92]. [cite_start]To address this, PRAVAH employs the Synthetic Minority Over-sampling Technique (SMOTE) integrated with an Extreme Gradient Boosting (XGBoost) classifier[cite: 12].
* [cite_start]**Cost-Sensitive Classification**: The predictive core utilizes a strict, safety-focused decision boundary with a threshold of 0.25[cite: 13, 88]. [cite_start]This is algorithmically bound to a Dynamic Rain Factor to intentionally trade nominal precision for maximum life safety[cite: 13, 103].
* [cite_start]**Performance Insights**: The optimized Recall for flood events is 89%, demonstrating the capacity to correctly identify high-severity anomalies[cite: 14]. [cite_start]SHAP feature analysis confirms that the recent 7-day cumulative rainfall is the paramount predictor, reinforcing the critical role of antecedent moisture[cite: 15].

## Deployment Features
* [cite_start]**Backend**: The intelligence layer operates via a FastAPI backend, delivering probabilistic inferences as JSON payloads with sub-50 ms latency[cite: 16, 121].
* [cite_start]**Frontend**: An interactive Leaflet.js dashboard receives the backend data and visualizes actionable zonal risk levels[cite: 16, 173].
* [cite_start]**Emergency Management**: The dashboard is equipped with an Automated Response Protocol for real-time municipal emergency management, dispatching Standard Operating Procedures (SOPs) based on specific risk tiers[cite: 16, 123].

## Project Structure
* `backend/`: FastAPI application endpoints and caching.
* `dashboard/`: Leaflet.js UI, styles, and visualization logic.
* `datasets/`: Extracted and processed data (excluded from version control).
* `models/`: Trained XGBoost and Random Forest `.pkl` files (excluded from version control).
* `training/`: Feature engineering, model evaluation, and pipeline scripts.

## Setup Instructions
1. Clone the repository.
2. Create and activate a virtual environment: `python -m venv venv`
3. Install dependencies: `pip install -r requirements.txt`
4. Note: Static structural topological data and models must be generated locally as they are excluded from the repository.

## Authors
* [cite_start]Gautam Kumar [cite: 2]
* [cite_start]Maddula P V N Sai Sri Akshay [cite: 5]
* [cite_start]Hema Sri [cite: 6]
* [cite_start]Parampreet Kaur [cite: 18]
* [cite_start]Hemanth Boddupally [cite: 21]