import geopandas as gpd
import folium
from shapely.geometry import box

print("Loading Chennai boundary...")

gdf = gpd.read_file("datasets/maps/chennai_boundary.geojson")

# get bounds
minx, miny, maxx, maxy = gdf.total_bounds

# create horizontal slices
north_box = box(minx, (miny+maxy)/2, maxx, maxy)
central_box = box(minx, (miny+maxy)/3, maxx, (miny+maxy)/2)
south_box = box(minx, miny, maxx, (miny+maxy)/3)

# clip slices with actual Chennai boundary
north = gdf.geometry.intersection(north_box)
central = gdf.geometry.intersection(central_box)
south = gdf.geometry.intersection(south_box)

zones = {
    "North Chennai": north,
    "Central Chennai": central,
    "South Chennai": south
}

# example risk values
zone_risk = {
    "North Chennai": 0.75,
    "Central Chennai": 0.45,
    "South Chennai": 0.25
}

# create map
m = folium.Map(location=[13.0827, 80.2707], zoom_start=11)

for zone_name, geom in zones.items():

    risk = zone_risk[zone_name]

    if risk > 0.7:
        color = "red"
        level = "High"
    elif risk > 0.4:
        color = "orange"
        level = "Moderate"
    else:
        color = "green"
        level = "Low"

    folium.GeoJson(
        geom,
        style_function=lambda x, color=color: {
            "fillColor": color,
            "color": "black",
            "weight": 2,
            "fillOpacity": 0.6,
        },
        tooltip=f"{zone_name} | Risk: {level} | Probability: {risk}"
    ).add_to(m)

m.save("flood_risk_map.html")

print("Improved flood risk map created!")