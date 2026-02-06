import pandas as pd
import folium
from geopy.geocoders import Nominatim
from folium.plugins import MarkerCluster
import time

def create_lotto_map(input_file="lotto_results_kinov.xlsx", output_file="lotto_map.html"):
    # 1. Load Data
    try:
        df = pd.read_excel(input_file)
    except FileNotFoundError:
        print(f"Error: {input_file} not found. Please run scraper_v2.py first.")
        return

    print(f"Loaded {len(df)} records.")

    # 2. Group by Shop to count frequency
    # We use Shop Name and Address as unique key
    shop_counts = df.groupby(['상호명', '소재지']).size().reset_index(name='당첨횟수')
    
    # 3. Geocoding Setup
    geolocator = Nominatim(user_agent="lotto_map_visualizer_kinov_demo")
    
    # Base Map (Starting at center of Korea approx)
    m = folium.Map(location=[36.5, 127.5], zoom_start=7)
    marker_cluster = MarkerCluster().add_to(m)

    print("Geocoding addresses...")
    
    success_count = 0
    for index, row in shop_counts.iterrows():
        name = row['상호명']
        address = row['소재지']
        count = row['당첨횟수']
        
        # Clean address for better geocoding match
        # Remove "1층", "지하" etc usually helps, but try raw first then clean if fail?
        # Simple cleaning strategy: remove common suffixes if simple geocode fails could be added.
        # For now, let's try the raw address, maybe strip "1층" if it's at the end.
        clean_address = address.split(" 1층")[0].split("지하")[0].strip()
        
        try:
            location = geolocator.geocode(clean_address, timeout=10)
            if location:
                # Create detailed popup text
                popup_text = f"""
                <div style="width:200px">
                    <b>{name}</b><br>
                    {address}<br>
                    <br>
                    <b>1등 당첨: {count}회</b>
                </div>
                """
                
                # Check 1207 1st place specific highlighting? 
                # User mentioned "서울 강서구 곰달래로25길 57 1층" specifically.
                
                # Marker Icon - Red for multiple wins, Blue for single
                icon_color = 'red' if count > 1 else 'blue'
                icon = folium.Icon(color=icon_color, icon='star')
                
                folium.Marker(
                    location=[location.latitude, location.longitude],
                    popup=folium.Popup(popup_text, max_width=300),
                    tooltip=f"{name} ({count}회)",
                    icon=icon
                ).add_to(marker_cluster)
                
                success_count += 1
            else:
                print(f"Failed to geocode: {name} - {clean_address}")
                # Fallback: maybe print a warning or Manual override for known failure
        except Exception as e:
            print(f"Error geocoding {name}: {e}")
        
        # Respect Usage Policy
        time.sleep(1) 

    # 4. Save Map
    m.save(output_file)
    print(f"Map saved to {output_file} with {success_count}/{len(shop_counts)} markers.")

if __name__ == "__main__":
    create_lotto_map()
