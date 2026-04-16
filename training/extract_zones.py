import osmnx as ox
import geopandas as gpd

def fetch_chennai_zones():
    print("🌍 Rerouting to OpenStreetMap Backup Servers...")
    ox.settings.timeout = 300 
    ox.settings.overpass_endpoint = 'https://overpass.kumi.systems/api/interpreter'
    
    place_name = "Chennai District, Tamil Nadu, India"
    
    tags = {
        'boundary': 'administrative',
        'admin_level': '10' 
    }
    
    try:
        print("📡 Downloading City Wards...")
        zones = ox.features_from_place(place_name, tags)
        zones = zones[zones.geometry.type.isin(['Polygon', 'MultiPolygon'])]
        
        # --- THE STRICT AREA FILTER ---
        zones_metric = zones.to_crs(epsg=3857)
        
        # 15 sq km = 15,000,000 sq meters. 
        # This violently cuts out any parent "Zones" and ONLY keeps the tiny "Wards"
        zones = zones[zones_metric.area < 15_000_000]
        
        if 'name' in zones.columns:
            clean_zones = zones[['name', 'geometry']].copy()
            clean_zones['name'] = clean_zones['name'].fillna("Unnamed Ward")
        else:
            clean_zones = zones[['geometry']].copy()
            clean_zones['name'] = [f"Ward_{i}" for i in range(len(zones))]
            
        output_filename = "chennai_zones.geojson"
        clean_zones.to_file(output_filename, driver="GeoJSON")
        
        print(f"✅ Success! Extracted {len(clean_zones)} strict city wards.")
        print(f"🗑️ Aggressively deleted any polygon larger than 15 sq km.")
        
    except Exception as e:
        print(f"❌ Error extracting data: {e}")

if __name__ == "__main__":
    fetch_chennai_zones()