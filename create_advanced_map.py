import pandas as pd
import folium
from folium.plugins import MarkerCluster
from geopy.geocoders import Nominatim
import time
import json
from pathlib import Path

def geocode_addresses(df, cache_file="geocoded_cache.xlsx"):
    """Geocode addresses with caching"""
    geolocator = Nominatim(user_agent="kinov_lotto_advanced_v3")
    
    # Load cache if exists
    cache = {}
    if Path(cache_file).exists():
        cache_df = pd.read_excel(cache_file)
        for _, row in cache_df.iterrows():
            cache[row['소재지']] = (row['lat'], row['lon'])
        print(f"Loaded {len(cache)} cached locations")
    
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
    
    print(f"Processing {len(shop_data)} unique locations...")
    
    for idx, row in shop_data.iterrows():
        name = row['상호명']
        address = row['소재지']
        
        # Check cache first
        if address in cache:
            lat, lon = cache[address]
            geocoded_data.append({
                '상호명': name,
                '소재지': address,
                'lat': lat,
                'lon': lon,
                '당첨횟수': row['당첨횟수'],
                '자동횟수': row['자동횟수'],
                '수동횟수': row['수동횟수'],
                '회차목록': row['회차'],
                '방식목록': row['당첨방식']
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
                    '상호명': name,
                    '소재지': address,
                    'lat': lat,
                    'lon': lon,
                    '당첨횟수': row['당첨횟수'],
                    '자동횟수': row['자동횟수'],
                    '수동횟수': row['수동횟수'],
                    '회차목록': row['회차'],
                    '방식목록': row['당첨방식']
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
            cache_df = pd.read_excel(cache_file)
            cache_df = pd.concat([cache_df, pd.DataFrame(new_geocodes)], ignore_index=True)
        else:
            cache_df = pd.DataFrame(new_geocodes)
        cache_df.to_excel(cache_file, index=False)
        print(f"Saved {len(new_geocodes)} new geocodes to cache")
    
    return pd.DataFrame(geocoded_data)

def create_advanced_map(input_file="lotto_results_kinov.xlsx", 
                       output_file="lotto_advanced_map.html"):
    """Create advanced interactive map with real-time filtering"""
    
    print("=" * 60)
    print("KINOV Lotto Map Generator - Advanced Edition")
    print("=" * 60)
    
    # Load data
    print("\nLoading lottery data...")
    df = pd.read_excel(input_file)
    print(f"   - Loaded {len(df):,} records")
    print(f"   - Rounds: {df['회차'].min()} ~ {df['회차'].max()}")
    print(f"   - Unique shops: {df.groupby(['상호명', '소재지']).ngroups:,}")
    
    # Geocode
    print("\nGeocoding addresses...")
    geocoded_df = geocode_addresses(df)
    print(f"   - Successfully geocoded: {len(geocoded_df):,} locations")
    
    # Create map
    print("\nCreating interactive map...")
    m = folium.Map(
        location=[36.5, 127.5],
        zoom_start=7,
        tiles='OpenStreetMap',
        control_scale=True
    )
    
    # Prepare full dataset for JavaScript
    all_records = []
    for _, row in df.iterrows():
        # Find geocoded location
        geo = geocoded_df[
            (geocoded_df['상호명'] == row['상호명']) & 
            (geocoded_df['소재지'] == row['소재지'])
        ]
        if not geo.empty:
            all_records.append({
                'round': int(row['회차']),
                'name': row['상호명'],
                'address': row['소재지'],
                'method': row['당첨방식'],
                'lat': float(geo.iloc[0]['lat']),
                'lon': float(geo.iloc[0]['lon'])
            })
    
    # Embed data and create dynamic map
    map_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>KINOV Lotto Winners Map</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css" />
        <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css" />
        <style>
            body {{ margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; }}
            #map {{ position: absolute; top: 0; bottom: 0; width: 100%; }}
            
            #filter-panel {{
                position: absolute;
                top: 10px;
                right: 10px;
                background: white;
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                z-index: 1000;
                width: 320px;
                max-height: 90vh;
                overflow-y: auto;
            }}
            
            h3 {{ margin: 0 0 15px 0; color: #d32f2f; font-size: 18px; }}
            
            .filter-group {{
                margin-bottom: 15px;
                padding-bottom: 15px;
                border-bottom: 1px solid #eee;
            }}
            
            .filter-group:last-of-type {{ border-bottom: none; }}
            
            label {{ display: block; margin-bottom: 5px; font-weight: 600; font-size: 13px; color: #333; }}
            
            input[type="number"] {{
                width: 80px;
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 6px;
                font-size: 13px;
            }}
            
            input[type="checkbox"] {{
                margin-right: 5px;
                cursor: pointer;
            }}
            
            .range-inputs {{
                display: flex;
                gap: 10px;
                align-items: center;
            }}
            
            .checkbox-group {{
                display: flex;
                gap: 15px;
                flex-wrap: wrap;
            }}
            
            .checkbox-label {{
                display: flex;
                align-items: center;
                cursor: pointer;
                font-size: 13px;
            }}
            
            button {{
                width: 100%;
                padding: 12px;
                background: linear-gradient(135deg, #d32f2f 0%, #c62828 100%);
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-weight: bold;
                font-size: 14px;
                transition: all 0.3s;
            }}
            
            button:hover {{
                background: linear-gradient(135deg, #c62828 0%, #b71c1c 100%);
                transform: translateY(-1px);
                box-shadow: 0 4px 8px rgba(211, 47, 47, 0.3);
            }}
            
            button:active {{ transform: translateY(0); }}
            
            .stats-box {{
                margin-top: 15px;
                padding: 12px;
                background: linear-gradient(135deg, #f5f5f5 0%, #eeeeee 100%);
                border-radius: 8px;
                font-size: 12px;
            }}
            
            .stats-box p {{
                margin: 5px 0;
                display: flex;
                justify-content: space-between;
            }}
            
            .stats-value {{
                font-weight: bold;
                color: #d32f2f;
            }}
            
            .leaflet-popup-content {{
                margin: 15px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
        </style>
    </head>
    <body>
        <div id="map"></div>
        
        <div id="filter-panel">
            <h3>🎯 필터 설정</h3>
            
            <div class="filter-group">
                <label>📅 회차 범위</label>
                <div class="range-inputs">
                    <input type="number" id="round-min" value="{df['회차'].min()}" min="{df['회차'].min()}" max="{df['회차'].max()}">
                    <span>~</span>
                    <input type="number" id="round-max" value="{df['회차'].max()}" min="{df['회차'].min()}" max="{df['회차'].max()}">
                </div>
            </div>
            
            <div class="filter-group">
                <label>🎲 당첨 방식</label>
                <div class="checkbox-group">
                    <label class="checkbox-label">
                        <input type="checkbox" id="filter-auto" checked>
                        <span>🤖 자동</span>
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" id="filter-manual" checked>
                        <span>✋ 수동</span>
                    </label>
                </div>
            </div>
            
            <button id="apply-filter">🔍 필터 적용</button>
            
            <div class="stats-box">
                <p><span>전체 데이터:</span><span class="stats-value" id="total-count">{len(all_records):,}</span></p>
                <p><span>표시 중:</span><span class="stats-value" id="filtered-count">{len(all_records):,}</span></p>
                <p><span>점포 수:</span><span class="stats-value" id="shop-count">{len(geocoded_df):,}</span></p>
            </div>
        </div>
        
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>
        <script>
            // Data
            const allData = {json.dumps(all_records, ensure_ascii=False)};
            
            // Initialize map
            const map = L.map('map').setView([36.5, 127.5], 7);
            
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
                maxZoom: 19
            }}).addTo(map);
            
            let markerCluster = null;
            
            // Marker color/icon functions
            function getMarkerColor(count) {{
                if (count >= 5) return 'red';
                if (count >= 3) return 'orange';
                if (count >= 2) return 'blue';
                return 'green';
            }}
            
            function getMarkerIcon(count) {{
                const color = getMarkerColor(count);
                return L.icon({{
                    iconUrl: `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-${{color}}.png`,
                    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
                    iconSize: [25, 41],
                    iconAnchor: [12, 41],
                    popupAnchor: [1, -34],
                    shadowSize: [41, 41]
                }});
            }}
            
            // Update map with filtered data
            function updateMap() {{
                const minRound = parseInt(document.getElementById('round-min').value);
                const maxRound = parseInt(document.getElementById('round-max').value);
                const showAuto = document.getElementById('filter-auto').checked;
                const showManual = document.getElementById('filter-manual').checked;
                
                // Filter data
                const filtered = allData.filter(item => {{
                    const roundMatch = item.round >= minRound && item.round <= maxRound;
                    const methodMatch = (showAuto && item.method === '자동') || 
                                       (showManual && item.method === '수동');
                    return roundMatch && methodMatch;
                }});
                
                // Group by location
                const locationMap = {{}};
                filtered.forEach(item => {{
                    const key = `${{item.name}}|${{item.address}}`;
                    if (!locationMap[key]) {{
                        locationMap[key] = {{
                            name: item.name,
                            address: item.address,
                            lat: item.lat,
                            lon: item.lon,
                            rounds: [],
                            methods: [],
                            autoCount: 0,
                            manualCount: 0
                        }};
                    }}
                    locationMap[key].rounds.push(item.round);
                    locationMap[key].methods.push(item.method);
                    if (item.method === '자동') locationMap[key].autoCount++;
                    if (item.method === '수동') locationMap[key].manualCount++;
                }});
                
                // Clear existing markers
                if (markerCluster) {{
                    map.removeLayer(markerCluster);
                }}
                
                markerCluster = L.markerClusterGroup({{
                    chunkedLoading: true,
                    spiderfyOnMaxZoom: true,
                    showCoverageOnHover: false,
                    zoomToBoundsOnClick: true
                }});
                
                // Add markers
                Object.values(locationMap).forEach(loc => {{
                    const count = loc.rounds.length;
                    const icon = getMarkerIcon(count);
                    
                    const sortedRounds = loc.rounds.sort((a, b) => b - a);
                    const roundsText = sortedRounds.slice(0, 10).join(', ') + 
                                      (sortedRounds.length > 10 ? ` 외 ${{sortedRounds.length - 10}}회` : '');
                    
                    const popupContent = `
                        <div style="min-width: 250px;">
                            <h4 style="margin: 0 0 10px 0; color: #d32f2f; font-size: 16px;">🎰 ${{loc.name}}</h4>
                            <hr style="margin: 8px 0; border: none; border-top: 1px solid #eee;">
                            <p style="margin: 5px 0; font-size: 13px;"><b>📍 주소:</b><br>${{loc.address}}</p>
                            <hr style="margin: 8px 0; border: none; border-top: 1px solid #eee;">
                            <p style="margin: 5px 0; font-size: 15px;"><b>🏆 총 당첨:</b> <span style="color: #d32f2f; font-weight: bold;">${{count}}회</span></p>
                            <p style="margin: 5px 0; font-size: 13px;"><b>🤖 자동:</b> ${{loc.autoCount}}회 | <b>✋ 수동:</b> ${{loc.manualCount}}회</p>
                            <hr style="margin: 8px 0; border: none; border-top: 1px solid #eee;">
                            <p style="margin: 5px 0; font-size: 12px; color: #666;"><b>당첨 회차:</b><br>${{roundsText}}</p>
                        </div>
                    `;
                    
                    const marker = L.marker([loc.lat, loc.lon], {{ icon: icon }})
                        .bindPopup(popupContent)
                        .bindTooltip(`${{loc.name}} (${{count}}회)`, {{ direction: 'top' }});
                    
                    markerCluster.addLayer(marker);
                }});
                
                map.addLayer(markerCluster);
                
                // Update stats
                document.getElementById('filtered-count').textContent = filtered.length.toLocaleString();
                document.getElementById('shop-count').textContent = Object.keys(locationMap).length.toLocaleString();
            }}
            
            // Event listeners
            document.getElementById('apply-filter').addEventListener('click', updateMap);
            
            // Initial render
            updateMap();
        </script>
    </body>
    </html>
    """
    
    # Save
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(map_html)
    
    print(f"   - Map created successfully!")
    print("\n" + "=" * 60)
    print(f"SUCCESS! Map saved to: {output_file}")
    print("=" * 60)
    print(f"\nStatistics:")
    print(f"   - Total records: {len(all_records):,}")
    print(f"   - Unique shops: {len(geocoded_df):,}")
    print(f"   - Round range: {df['회차'].min()} ~ {df['회차'].max()}")
    print(f"\nFeatures:")
    print(f"   - Zoom-based clustering")
    print(f"   - Color-coded markers (green=1, blue=2-3, orange=3-4, red=5+)")
    print(f"   - Real-time filtering (round range, auto/manual)")
    print(f"   - Detailed popups with win history")
    print(f"\nOpen {output_file} in your browser to explore!")
    
    return output_file

if __name__ == "__main__":
    create_advanced_map()
