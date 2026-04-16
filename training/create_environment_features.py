import pandas as pd
import geopandas as gpd

# Load rainfall features
rainfall = pd.read_csv("datasets/processed/rainfall_with_flood_labels.csv")

# Load elevation values
elevation = pd.read_csv("datasets/processed/chennai_elevation_values.csv")

# Load drainage network
drainage = gpd.read_file("datasets/processed/chennai_drainage_network.geojson")

# Load vegetation
vegetation = gpd.read_file("datasets/processed/chennai_vegetation.geojson")

# Calculate environmental metrics
mean_elevation = elevation["elevation_m"].mean()

drainage_density = len(drainage)

vegetation_density = len(vegetation)

print("Environmental features:")
print("Mean elevation:", mean_elevation)
print("Drainage features:", drainage_density)
print("Vegetation features:", vegetation_density)

# Add environmental features to rainfall dataset
rainfall["mean_elevation"] = mean_elevation
rainfall["drainage_density"] = drainage_density
rainfall["vegetation_density"] = vegetation_density

# Save final dataset
rainfall.to_csv("datasets/processed/pravah_master_dataset.csv", index=False)

print("PRAVAH master dataset created successfully")