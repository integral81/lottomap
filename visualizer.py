import pandas as pd
import folium
from folium.plugins import MarkerCluster
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import time

def create_lotto_map(input_file, start_round, end_round, output_file="lotto_map_test.html"):
    print(f"Loading data from {input_file}...")
    try:
        df = pd.read_excel(input_file)
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return

    # Filter data for the requested test range
    # Ensure '회차' column is numeric
    df['회차'] = pd.to_numeric(df['회차'], errors='coerce')
    target_df = df[(df['회차'] >= start_round) & (df['회차'] <= end_round)].copy()
    
    print(f"Filtered {len(target_df)} winners from Round {start_round} to {end_round}.")

    if target_df.empty:
        print("No data found for the specified range.")
        return

    # Initialize Geocoder with longer timeout
    # user_agent is required by Nominatim policy
    geolocator = Nominatim(user_agent="lotto_map_visualizer_kinov_v2", timeout=10)
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=2)

    # Dictionary to cache coordinates to save time if addresses repeat
    location_cache = {}

    print("Geocoding addresses (this may take a moment)...")
    
    # Simple coordinates function with retry
    def get_lat_lon(addr):
        if addr in location_cache:
            return location_cache[addr]
        
        retries = 3
        for attempt in range(retries):
            try:
                # Adding 'South Korea' helps accuracy if not present
                search_addr = addr if "대한민국" in addr or "한국" in addr else f"대한민국 {addr}"
                location = geocode(search_addr)
                if location:
                    res = (location.latitude, location.longitude)
                    location_cache[addr] = res
                    return res
                else:
                    return None # Address not found
            except Exception as e:
                print(f"  Geocoding error for '{addr}' (Attempt {attempt+1}/{retries}): {e}")
                time.sleep(2) # Wait before retry
        
        return None

    # Apply geocoding
    # Using a loop to have better progress visibility
    stats = {"success": 0, "fail": 0}
    coordinates = []
    
    for idx, row in target_df.iterrows():
        addr = row['소재지']
        coords = get_lat_lon(addr)
        if coords:
            coordinates.append(coords)
            stats["success"] += 1
        else:
            coordinates.append((None, None))
            stats["fail"] += 1
            print(f"Failed to geocode: {addr}")
            
    target_df['lat'] = [c[0] for c in coordinates]
    target_df['lon'] = [c[1] for c in coordinates]

    # Drop rows without coordinates
    map_df = target_df.dropna(subset=['lat', 'lon'])

    # Create Base Map
    # Center map on the average location or a default Seoul location
    if not map_df.empty:
        center_lat = map_df['lat'].mean()
        center_lon = map_df['lon'].mean()
        m = folium.Map(location=[center_lat, center_lon], zoom_start=7)
    else:
        m = folium.Map(location=[36.5, 127.5], zoom_start=7) # Korea center

    # Add markers
    marker_cluster = MarkerCluster().add_to(m)

    for idx, row in map_df.iterrows():
        popup_content = f"""
        <div style="width:200px">
            <b>{row['상호명']}</b><br>
            회차: {row['회차']}회<br>
            방식: {row['당첨방식']}<br>
            주소: {row['소재지']}
        </div>
        """
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=folium.Popup(popup_content, max_width=300),
            tooltip=row['상호명'],
            icon=folium.Icon(color='blue', icon='star')
        ).add_to(marker_cluster)

    # Save map
    m.save(output_file)
    print(f"\nMap saved to {output_file}")
    print(f"Geocoding Stats: Success={stats['success']}, Failed={stats['fail']}")

if __name__ == "__main__":
    # Prioritize testing with 1207-1209 results as requested
    create_lotto_map("lotto_results_kinov.xlsx", 1207, 1209)
