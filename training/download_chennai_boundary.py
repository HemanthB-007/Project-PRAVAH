import osmnx as ox
import geopandas as gpd

place_name = "Chennai, Tamil Nadu, India"

print("Downloading Chennai boundary...")

gdf = ox.geocode_to_gdf(place_name)

print("Boundary downloaded")

gdf.to_file("datasets/maps/chennai_boundary.geojson", driver="GeoJSON")

print("Saved to datasets/maps/chennai_boundary.geojson")