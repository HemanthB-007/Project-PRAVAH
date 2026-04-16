import osmnx as ox
import geopandas as gpd

place_name = "Chennai, Tamil Nadu, India"

# vegetation-related land use tags
tags = {
    "landuse": ["forest", "grass", "meadow", "park"],
    "natural": ["wood", "wetland"]
}

print("Downloading vegetation features for Chennai...")

gdf = ox.features_from_place(place_name, tags)

print("Total vegetation features:", len(gdf))

gdf.to_file("datasets/processed/chennai_vegetation.geojson", driver="GeoJSON")

print("Vegetation dataset extracted successfully")