import osmnx as ox
import geopandas as gpd

# define Chennai location
place_name = "Chennai, Tamil Nadu, India"

# download waterways from OpenStreetMap
tags = {"waterway": True}

print("Downloading drainage network for Chennai...")

gdf = ox.features_from_place(place_name, tags)

# keep only line geometries (rivers, streams etc.)
gdf = gdf[gdf.geometry.type.isin(["LineString", "MultiLineString"])]

print("Total drainage features:", len(gdf))

# save dataset
gdf.to_file("datasets/processed/chennai_drainage_network.geojson", driver="GeoJSON")

print("Drainage network extracted successfully")