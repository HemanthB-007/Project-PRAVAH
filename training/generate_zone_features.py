import pandas as pd
import geopandas as gpd
import numpy as np
import os

def create_zone_lookup():
    print("🌍 Loading Chennai Zones...")
    
    # Path to your newly moved geojson
    geojson_path = "../datasets/processed/chennai_zones.geojson"
    
    if not os.path.exists(geojson_path):
        print(f"❌ Cannot find {geojson_path}. Make sure you moved it!")
        return

    # Load the geojson
    gdf = gpd.read_file(geojson_path)
    
    # Create an empty list to store our features
    features = []
    
    # Set a random seed so the numbers stay the same every time you run it
    np.random.seed(42)
    
    for index, row in gdf.iterrows():
        # Get the zone name (fallback to Zone_ID if unnamed)
        zone_name = row.get('name', f"Zone_{index}")
        if pd.isna(zone_name):
            zone_name = f"Zone_{index}"
            
        # Generate realistic mock data for Chennai's topography
        # Elevation: Chennai is very flat, mostly between 1m and 15m above sea level
        elevation = round(np.random.uniform(0.5, 14.5), 2)
        
        # Drainage Density: Between 0.2 (Poor) and 0.8 (Good)
        drainage = round(np.random.uniform(0.2, 0.8), 2)
        
        # Vegetation Density: Between 0.1 (Concrete Jungle) and 0.7 (Parks/Wetlands)
        vegetation = round(np.random.uniform(0.1, 0.7), 2)
        
        features.append({
            "zone_id": str(index), # Keep a unique ID to link with the map later
            "zone_name": zone_name,
            "mean_elevation": elevation,
            "drainage_density": drainage,
            "vegetation_density": vegetation
        })
        
    # Convert to DataFrame
    df = pd.DataFrame(features)
    
    # Save to CSV
    output_path = "../datasets/processed/zone_features_lookup.csv"
    df.to_csv(output_path, index=False)
    
    print(f"✅ Success! Generated static features for {len(df)} zones.")
    print(f"📁 Saved lookup table to: {output_path}")

if __name__ == "__main__":
    create_zone_lookup()