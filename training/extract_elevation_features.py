import rasterio
import numpy as np
import pandas as pd

# load DEM file
dem_path = "datasets/elevation/chennai_dem.tif"

with rasterio.open(dem_path) as dataset:
    elevation = dataset.read(1)
    transform = dataset.transform

# remove invalid values
elevation = elevation[elevation > -100]

# calculate basic stats
mean_elevation = np.mean(elevation)
min_elevation = np.min(elevation)
max_elevation = np.max(elevation)

print("Elevation statistics")
print("Mean elevation:", mean_elevation)
print("Min elevation:", min_elevation)
print("Max elevation:", max_elevation)

# convert elevation grid to dataframe
elevation_values = elevation.flatten()
elevation_values = elevation_values[elevation_values > -100]

df = pd.DataFrame({
    "elevation_m": elevation_values
})

# save processed elevation dataset
df.to_csv("datasets/processed/chennai_elevation_values.csv", index=False)

print("Elevation dataset saved successfully")