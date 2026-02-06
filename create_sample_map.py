import pandas as pd
import folium
from folium.plugins import MarkerCluster
from geopy.geocoders import Nominatim
import time
import json
from pathlib import Path

def geocode_addresses(df, cache_file="geocoded_cache.xlsx"):
    """Geocode addresses with caching"""
    geolocator = Nominatim(user_agent="kinov_lotto_sample_v1")
    
    # Load cache if exists
    cache = {}
    if Path(cache_file).exists():
        try:
            cache_df = pd.read_excel(cache_file)
            for _, row in cache_df.iterrows():
                cache[row['소재지']] = (row['lat'], row['lon'])
            print(f"Loaded {len(cache)} cached locations")
        except:
            pass
    
    # Group by shop
    shop_data = df.groupby(['상호명', '소재지']).agg({
        '회차': list,
        '당첨방식': list
    }).reset_index()
    
    shop_data['당첨횟수'] = shop_data['회차'].apply(len)
    shop_data['자동횟수'] = shop_data['당첨방식'].apply(lambda x: x.count('자동'))
    shop_data['수동횟수'] = shop_data['당첨방식'].apply(lambda x: x.count('수동'))
    
    geocoded_data = []
    new_geocodes = []
    
    print(f"Processing {len(shop_data)} unique locations for sample...")
    
    for idx, row in shop_data.iterrows():
        name = row['상호명']
        address = row['소재지']
        
        # Check cache first
        if address in cache:
            lat, lon = cache[address]
            geocoded_data.append({
                '상호명': name, '소재지': address, 'lat': lat, 'lon': lon,
                '당첨횟수': row['당첨횟수'], '자동횟수': row['자동횟수'], '수동횟수': row['수동횟수'],
                '회차목록': row['회차'], '방식목록': row['당첨방식']
            })
            print(f"[CACHED] {idx+1}/{len(shop_data)}: {name}")
            continue
        
        # Geocode new address
        clean_address = address.split(" 1층")[0].split("지하")[0].strip()
        
        try:
            location = geolocator.geocode(clean_address, timeout=10)
            if location:
                lat, lon = location.latitude, location.longitude
                geocoded_data.append({
                    '상호명': name, '소재지': address, 'lat': lat, 'lon': lon,
                    '당첨횟수': row['당첨횟수'], '자동횟수': row['자동횟수'], '수동횟수': row['수동횟수'],
                    '회차목록': row['회차'], '방식목록': row['당첨방식']
                })
                new_geocodes.append({'소재지': address, 'lat': lat, 'lon': lon})
                print(f"[NEW] {idx+1}/{len(shop_data)}: {name}")
            else:
                print(f"[FAILED] {idx+1}/{len(shop_data)}: {name}")
        except Exception as e:
            print(f"[ERROR] {idx+1}/{len(shop_data)}: {name} - {str(e)[:50]}")
        
        time.sleep(1)
    
    # Update cache
    if new_geocodes:
        if Path(cache_file).exists():
            try:
                cache_df = pd.read_excel(cache_file)
                cache_df = pd.concat([cache_df, pd.DataFrame(new_geocodes)], ignore_index=True).drop_duplicates(subset=['소재지'])
            except:
                cache_df = pd.DataFrame(new_geocodes)
        else:
            cache_df = pd.DataFrame(new_geocodes)
        cache_df.to_excel(cache_file, index=False)
        print(f"Saved {len(new_geocodes)} new geocodes to cache")
    
    return pd.DataFrame(geocoded_data)

def create_sample_map(input_file="lotto_results_kinov.xlsx", output_file="lotto_recent_3_rounds.html"):
    print("Loading lottery data for sample (Recent 3 Rounds)...")
    df = pd.read_excel(input_file)
    
    # Filter for last 3 rounds
    recent_rounds = sorted(df['회차'].unique())[-3:]
    df_sample = df[df['회차'].isin(recent_rounds)]
    
    print(f"Filtered for rounds: {recent_rounds}")
    print(f"Sample data size: {len(df_sample)} records")
    
    geocoded_df = geocode_addresses(df_sample)
    
    # JavaScript data preparation
    all_records = []
    for _, row in df_sample.iterrows():
        geo = geocoded_df[(geocoded_df['상호명'] == row['상호명']) & (geocoded_df['소재지'] == row['소재지'])]
        if not geo.empty:
            all_records.append({
                'round': int(row['회차']),
                'name': row['상호명'],
                'address': row['소재지'],
                'method': row['당첨방식'],
                'lat': float(geo.iloc[0]['lat']),
                'lon': float(geo.iloc[0]['lon'])
            })

    # The HTML part is identical to the advanced map for consistency
    map_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>KINOV Lotto Winners Map (Recent 3 Rounds)</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css" />
        <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css" />
        <style>
            body {{ margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; }}
            #map {{ position: absolute; top: 0; bottom: 0; width: 100%; }}
            #filter-panel {{
                position: absolute; top: 10px; right: 10px; background: white; padding: 20px;
                border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); z-index: 1000;
                width: 320px; max-height: 90vh; overflow-y: auto;
            }}
            h4 {{ margin: 0 0 10px 0; color: #d32f2f; font-size: 16px; }}
            .stats-box {{ margin-top: 15px; padding: 12px; background: #f5f5f5; border-radius: 8px; font-size: 12px; }}
            .stats-value {{ font-weight: bold; color: #d32f2f; }}
            button {{ width: 100%; padding: 10px; background: #d32f2f; color: white; border: none; border-radius: 6px; cursor: pointer; }}
        </style>
    </head>
    <body>
        <div id="map"></div>
        <div id="filter-panel">
            <h3>🎯 샘플 필터 (최근 3회차)</h3>
            <div id="stats" class="stats-box">
                <p>회차: {recent_rounds[0]} ~ {recent_rounds[-1]}</p>
                <p>표시 중: <span id="filtered-count">0</span>건</p>
            </div>
            <button onclick="location.reload()">새로고침</button>
        </div>
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>
        <script>
            const allData = {json.dumps(all_records, ensure_ascii=False)};
            const map = L.map('map').setView([36.5, 127.5], 7);
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png').addTo(map);
            
            const markerCluster = L.markerClusterGroup();
            const locationMap = {{}};
            
            allData.forEach(item => {{
                const key = `${{item.name}}|${{item.address}}`;
                if (!locationMap[key]) {{
                    locationMap[key] = {{ name: item.name, address: item.address, lat: item.lat, lon: item.lon, rounds: [] }};
                }}
                locationMap[key].rounds.push(item.round);
            }});

            Object.values(locationMap).forEach(loc => {{
                const marker = L.marker([loc.lat, loc.lon])
                    .bindPopup(`<b>${{loc.name}}</b><br>${{loc.address}}<br>당첨회차: ${{loc.rounds.join(', ')}}`);
                markerCluster.addLayer(marker);
            }});
            
            map.addLayer(markerCluster);
            document.getElementById('filtered-count').textContent = allData.length;
        </script>
    </body>
    </html>
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(map_html)
    print(f"SUCCESS! Sample map saved to: {output_file}")

if __name__ == "__main__":
    create_sample_map()
