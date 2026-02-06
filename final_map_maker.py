import pandas as pd
import folium
from folium.plugins import MarkerCluster
import requests
import json
import time
from pathlib import Path

# --- CONFIGURATION ---
KAKAO_API_KEY = "d70d1805bba48840393cec5aa84bca53"
INPUT_FILE = "lotto_results_kinov_fresh.xlsx"
CACHE_FILE = "geocoded_cache.xlsx"
OUTPUT_FILE = "lotto_final_map.html"

def get_kakao_geocode(address):
    """Fetch coordinates from Kakao REST API"""
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
    params = {"query": address}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data['documents']:
                node = data['documents'][0]
                return float(node['y']), float(node['x'])
        return None, None
    except Exception as e:
        print(f"Error fetching {address}: {e}")
        return None, None

def process_geocoding(df):
    """Process all unique addresses with Kakao API and caching"""
    # Load cache
    cache = {}
    if Path(CACHE_FILE).exists():
        try:
            cache_df = pd.read_excel(CACHE_FILE)
            for _, row in cache_df.iterrows():
                cache[row['소재지']] = (row['lat'], row['lon'])
            print(f"Loaded {len(cache)} cached locations from {CACHE_FILE}", flush=True)
        except:
            print("Failed to load existing cache.")

    shop_data = df.groupby(['상호명', '소재지']).agg({
        '회차': list,
        '당첨방식': list
    }).reset_index()
    
    geocoded_list = []
    new_items = []
    total_shops = len(shop_data)
    print(f"Total unique shops to process: {total_shops}", flush=True)
    
    for idx, row in shop_data.iterrows():
        name = row['상호명']
        address = row['소재지']
        
        lat, lon = None, None
        if address in cache:
            lat, lon = cache[address]
        else:
            clean_addr = address.split(" 1층")[0].split("지하")[0].strip()
            lat, lon = get_kakao_geocode(clean_addr)
            
            if lat and lon:
                cache[address] = (lat, lon)
                new_items.append({'소재지': address, 'lat': lat, 'lon': lon})
                print(f"[OK] {idx+1}/{total_shops}: {name}", flush=True)
                if len(new_items) % 50 == 0:
                    # Incremental save
                    temp_df = pd.DataFrame(new_items)
                    if Path(CACHE_FILE).exists():
                        try:
                            old = pd.read_excel(CACHE_FILE)
                            temp_df = pd.concat([old, temp_df], ignore_index=True).drop_duplicates(subset=['소재지'])
                        except: pass
                    temp_df.to_excel(CACHE_FILE, index=False)
                    print(f"Progress: {idx+1}/{total_shops} ({len(new_items)} new geocodes saved)", flush=True)
            else:
                print(f"[FAIL] {idx+1}/{total_shops}: {name} ({clean_addr})", flush=True)
            
            time.sleep(0.1) # Safe rate limit

        if lat and lon:
            geocoded_list.append({
                '상호명': name, '소재지': address, 'lat': lat, 'lon': lon,
                '당첨횟수': len(row['회차']), '회차목록': row['회차'], '방식목록': row['당첨방식']
            })

    # Final cache save
    if new_items:
        final_cache = pd.DataFrame(list(cache.items()), columns=['소재지', 'coords'])
        final_cache['lat'] = final_cache['coords'].apply(lambda x: x[0])
        final_cache['lon'] = final_cache['coords'].apply(lambda x: x[1])
        final_cache[['소재지', 'lat', 'lon']].to_excel(CACHE_FILE, index=False)
        print(f"Final cache update complete. Total: {len(cache)}")

    return pd.DataFrame(geocoded_list)

def create_final_map():
    print("=" * 60)
    print("KINOV Lotto Map - Final Generation (Kakao API)")
    print("=" * 60)

    # 1. Load data
    if not Path(INPUT_FILE).exists():
        print(f"Error: {INPUT_FILE} not found!")
        return
    
    df = pd.read_excel(INPUT_FILE)
    print(f"Total Rows: {len(df)}")

    # 2. Geocode
    geo_df = process_geocoding(df)
    
    # 3. Build Marker Data for JS Filtering
    full_marker_data = []
    # Merge back to raw data to have per-round location info
    # (Easier for JS filtering by round)
    merged = df.merge(geo_df[['상호명', '소재지', 'lat', 'lon']], on=['상호명', '소재지'], how='inner')
    
    for _, row in merged.iterrows():
        full_marker_data.append({
            'r': int(row['회차']),
            'n': row['상호명'],
            'a': row['소재지'],
            'm': row['당첨방식'],
            'lat': float(row['lat']),
            'lng': float(row['lon'])
        })

    # 4. Create Map
    m = folium.Map(location=[36.5, 127.5], zoom_start=7)
    
    # Prepare HTML template with advanced UI
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>KINOV Lotto Final Map</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css" />
        <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css" />
        <style>
            body {{ margin: 0; font-family: 'Segoe UI', serif; }}
            #map {{ position: absolute; top: 0; bottom: 0; width: 100%; }}
            #panel {{
                position: absolute; top: 15px; right: 15px; background: white;
                padding: 20px; border-radius: 12px; box-shadow: 0 5px 15px rgba(0,0,0,0.2);
                z-index: 1000; width: 300px;
            }}
            h3 {{ margin: 0 0 15px; color: #d32f2f; font-size: 18px; text-align: center; }}
            .filter-sec {{ margin-bottom: 20px; }}
            .filter-title {{ font-weight: bold; margin-bottom: 8px; display: block; font-size: 14px; }}
            .inp-grp {{ display: flex; gap: 8px; align-items: center; }}
            input[type="number"] {{ width: 80px; padding: 6px; border: 1px solid #ddd; border-radius: 4px; }}
            .btn {{
                width: 100%; padding: 12px; background: #d32f2f; color: white;
                border: none; border-radius: 8px; cursor: pointer; font-weight: bold; margin-top: 10px;
            }}
            .stats {{ margin-top: 15px; background: #f9f9f9; padding: 10px; border-radius: 6px; font-size: 12px; }}
            .stats b {{ color: #d32f2f; }}
        </style>
    </head>
    <body>
        <div id="map"></div>
        <div id="panel">
            <h3>🎰 KINOV LOTTO MAP</h3>
            <div class="filter-sec">
                <span class="filter-title">📅 회차 범위</span>
                <div class="inp-grp">
                    <input type="number" id="minR" value="{df['회차'].min()}"> ~ 
                    <input type="number" id="maxR" value="{df['회차'].max()}">
                </div>
            </div>
            <div class="filter-sec">
                <span class="filter-title">🎲 당첨 방식</span>
                <label><input type="checkbox" id="chkA" checked> 자동</label> &nbsp;
                <label><input type="checkbox" id="chkM" checked> 수동</label>
            </div>
            <button class="btn" onclick="applyFilters()">필터 적용</button>
            <div class="stats">
                전체: <b>{len(full_marker_data):,}</b>건<br>
                현재: <b id="curCnt">-</b>건
            </div>
        </div>

        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>
        <script>
            const data = {json.dumps(full_marker_data, ensure_ascii=False)};
            const map = L.map('map').setView([36.5, 127.5], 7);
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png').addTo(map);
            
            let cluster = null;

            function getCol(c) {{
                if (c >= 10) return "darkred";
                if (c >= 5) return "red";
                if (c >= 3) return "orange";
                if (c >= 2) return "blue";
                return "green";
            }}

            function applyFilters() {{
                const min = parseInt(document.getElementById('minR').value);
                const max = parseInt(document.getElementById('maxR').value);
                const showA = document.getElementById('chkA').checked;
                const showM = document.getElementById('chkM').checked;

                if (cluster) map.removeLayer(cluster);
                cluster = L.markerClusterGroup({{ spiderfyOnMaxZoom: true, showCoverageOnHover: false }});

                const filtered = data.filter(d => {{
                    return d.r >= min && d.r <= max && 
                           ((showA && d.m === '자동') || (showM && d.m === '수동'));
                }});

                // Group by shop for marker display
                const shops = {{}};
                filtered.forEach(d => {{
                    const key = `${{d.n}}|${{d.a}}`;
                    if (!shops[key]) shops[key] = {{ n: d.n, a: d.a, lat: d.lat, lng: d.lng, r: [] }};
                    shops[key].r.push(d.r);
                }});

                Object.values(shops).forEach(s => {{
                    const cnt = s.r.length;
                    const col = getCol(cnt);
                    const marker = L.circleMarker([s.lat, s.lng], {{
                        radius: 8 + (cnt * 0.5),
                        fillColor: col, color: "#fff", weight: 2, fillOpacity: 0.8
                    }}).bindPopup(`
                        <div style="font-family: sans-serif;">
                            <h4 style="margin:0; color:${{col}}">${{s.n}}</h4>
                            <p style="margin:5px 0; font-size:12px;">${{s.a}}</p>
                            <hr>
                            <b>당첨 횟수: ${{cnt}}회</b><br>
                            회차: ${{s.r.sort((a,b)=>b-a).join(', ')}}
                        </div>
                    `);
                    cluster.addLayer(marker);
                }});

                map.addLayer(cluster);
                document.getElementById('curCnt').innerText = filtered.length.toLocaleString();
            }}

            applyFilters();
        </script>
    </body>
    </html>
    """
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"COMPLETE! Original: {len(df)} records.")
    print(f"Generated Map: {OUTPUT_FILE}")

if __name__ == "__main__":
    create_final_map()