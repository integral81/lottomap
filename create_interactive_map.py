import pandas as pd
import folium
from folium.plugins import MarkerCluster
from geopy.geocoders import Nominatim
import time
import json

def geocode_addresses(df):
    """Geocode addresses and cache results"""
    geolocator = Nominatim(user_agent="kinov_lotto_map_v2")
    
    # Group by shop to get unique locations
    shop_data = df.groupby(['상호명', '소재지']).agg({
        '회차': list,
        '당첨방식': list
    }).reset_index()
    
    shop_data['당첨횟수'] = shop_data['회차'].apply(len)
    shop_data['자동횟수'] = shop_data['당첨방식'].apply(lambda x: x.count('자동'))
    shop_data['수동횟수'] = shop_data['당첨방식'].apply(lambda x: x.count('수동'))
    
    geocoded_data = []
    
    print(f"Geocoding {len(shop_data)} unique locations...")
    
    for idx, row in shop_data.iterrows():
        name = row['상호명']
        address = row['소재지']
        
        # Clean address for better geocoding
        clean_address = address.split(" 1층")[0].split("지하")[0].strip()
        
        try:
            location = geolocator.geocode(clean_address, timeout=10)
            if location:
                geocoded_data.append({
                    '상호명': name,
                    '소재지': address,
                    'lat': location.latitude,
                    'lon': location.longitude,
                    '당첨횟수': row['당첨횟수'],
                    '자동횟수': row['자동횟수'],
                    '수동횟수': row['수동횟수'],
                    '회차목록': row['회차'],
                    '방식목록': row['당첨방식']
                })
                print(f"✓ {idx+1}/{len(shop_data)}: {name}")
            else:
                print(f"✗ {idx+1}/{len(shop_data)}: {name} - Geocoding failed")
        except Exception as e:
            print(f"✗ {idx+1}/{len(shop_data)}: {name} - Error: {e}")
        
        # Rate limiting
        time.sleep(1)
    
    return pd.DataFrame(geocoded_data)

def get_marker_color(count):
    """Determine marker color based on win count"""
    if count >= 5:
        return 'red'  # 5회 이상: 빨간색 (대박!)
    elif count >= 3:
        return 'orange'  # 3-4회: 주황색 (명당)
    elif count >= 2:
        return 'blue'  # 2회: 파란색 (행운)
    else:
        return 'green'  # 1회: 초록색 (일반)

def get_marker_icon(count):
    """Determine marker icon based on win count"""
    if count >= 5:
        return 'star'  # 5회 이상
    elif count >= 3:
        return 'certificate'  # 3-4회
    elif count >= 2:
        return 'heart'  # 2회
    else:
        return 'info-sign'  # 1회

def create_interactive_map(input_file="lotto_results_kinov.xlsx", 
                          geocoded_file="geocoded_locations.xlsx",
                          output_file="lotto_interactive_map.html"):
    """Create interactive map with filtering capabilities"""
    
    # Load data
    print("Loading lottery data...")
    df = pd.read_excel(input_file)
    print(f"Loaded {len(df)} records from {df['회차'].min()} to {df['회차'].max()} rounds")
    
    # Check if geocoded data exists
    try:
        geocoded_df = pd.read_excel(geocoded_file)
        print(f"Loaded {len(geocoded_df)} geocoded locations from cache")
    except FileNotFoundError:
        print("No cached geocoded data found. Starting geocoding...")
        geocoded_df = geocode_addresses(df)
        geocoded_df.to_excel(geocoded_file, index=False)
        print(f"Saved {len(geocoded_df)} geocoded locations to {geocoded_file}")
    
    # Create base map centered on South Korea
    m = folium.Map(
        location=[36.5, 127.5],
        zoom_start=7,
        tiles='OpenStreetMap'
    )
    
    # Create marker cluster
    marker_cluster = MarkerCluster(
        name='당첨점포 클러스터',
        overlay=True,
        control=True,
        show=True
    ).add_to(m)
    
    # Add markers
    print("Adding markers to map...")
    for idx, row in geocoded_df.iterrows():
        # Determine marker appearance
        color = get_marker_color(row['당첨횟수'])
        icon_name = get_marker_icon(row['당첨횟수'])
        
        # Create popup content
        popup_html = f"""
        <div style="width: 300px; font-family: Arial, sans-serif;">
            <h4 style="margin: 0 0 10px 0; color: #d32f2f;">🎰 {row['상호명']}</h4>
            <hr style="margin: 5px 0;">
            <p style="margin: 5px 0;"><b>📍 주소:</b> {row['소재지']}</p>
            <hr style="margin: 5px 0;">
            <p style="margin: 5px 0; font-size: 16px;"><b>🏆 총 당첨:</b> <span style="color: #d32f2f; font-weight: bold;">{row['당첨횟수']}회</span></p>
            <p style="margin: 5px 0;"><b>🤖 자동:</b> {row['자동횟수']}회 | <b>✋ 수동:</b> {row['수동횟수']}회</p>
            <hr style="margin: 5px 0;">
            <p style="margin: 5px 0; font-size: 12px;"><b>당첨 회차:</b><br>{', '.join(map(str, sorted(row['회차목록'], reverse=True)))}</p>
        </div>
        """
        
        # Create marker
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=folium.Popup(popup_html, max_width=350),
            tooltip=f"{row['상호명']} ({row['당첨횟수']}회)",
            icon=folium.Icon(
                color=color,
                icon=icon_name,
                prefix='glyphicon'
            )
        ).add_to(marker_cluster)
    
    # Prepare data for JavaScript filtering
    all_data = df.merge(
        geocoded_df[['상호명', '소재지', 'lat', 'lon']],
        on=['상호명', '소재지'],
        how='inner'
    )
    
    # Convert to JSON for embedding
    map_data = []
    for _, row in all_data.iterrows():
        map_data.append({
            '회차': int(row['회차']),
            '상호명': row['상호명'],
            '소재지': row['소재지'],
            '당첨방식': row['당첨방식'],
            'lat': float(row['lat']),
            'lon': float(row['lon'])
        })
    
    # Add custom HTML/CSS/JS for filtering
    filter_html = f"""
    <div id="filter-panel" style="
        position: fixed;
        top: 10px;
        right: 10px;
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        z-index: 1000;
        max-width: 350px;
        font-family: Arial, sans-serif;
    ">
        <h3 style="margin: 0 0 15px 0; color: #d32f2f;">🎯 필터 설정</h3>
        
        <div style="margin-bottom: 15px;">
            <label style="display: block; margin-bottom: 5px; font-weight: bold;">회차 범위:</label>
            <div style="display: flex; gap: 10px; align-items: center;">
                <input type="number" id="round-min" value="{df['회차'].min()}" min="{df['회차'].min()}" max="{df['회차'].max()}" 
                    style="width: 80px; padding: 5px; border: 1px solid #ccc; border-radius: 4px;">
                <span>~</span>
                <input type="number" id="round-max" value="{df['회차'].max()}" min="{df['회차'].min()}" max="{df['회차'].max()}"
                    style="width: 80px; padding: 5px; border: 1px solid #ccc; border-radius: 4px;">
            </div>
        </div>
        
        <div style="margin-bottom: 15px;">
            <label style="display: block; margin-bottom: 5px; font-weight: bold;">당첨 방식:</label>
            <div style="display: flex; gap: 10px;">
                <label style="display: flex; align-items: center; gap: 5px;">
                    <input type="checkbox" id="filter-auto" checked>
                    <span>🤖 자동</span>
                </label>
                <label style="display: flex; align-items: center; gap: 5px;">
                    <input type="checkbox" id="filter-manual" checked>
                    <span>✋ 수동</span>
                </label>
            </div>
        </div>
        
        <button id="apply-filter" style="
            width: 100%;
            padding: 10px;
            background: #d32f2f;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            font-size: 14px;
        ">필터 적용</button>
        
        <div id="filter-stats" style="
            margin-top: 15px;
            padding: 10px;
            background: #f5f5f5;
            border-radius: 5px;
            font-size: 12px;
        ">
            <p style="margin: 0;"><b>총 데이터:</b> <span id="total-count">{len(df)}</span>건</p>
            <p style="margin: 5px 0 0 0;"><b>필터 결과:</b> <span id="filtered-count">{len(df)}</span>건</p>
        </div>
    </div>
    
    <script>
        var allData = {json.dumps(map_data)};
        
        // This will be implemented in the next version with dynamic filtering
        document.getElementById('apply-filter').addEventListener('click', function() {{
            var minRound = parseInt(document.getElementById('round-min').value);
            var maxRound = parseInt(document.getElementById('round-max').value);
            var showAuto = document.getElementById('filter-auto').checked;
            var showManual = document.getElementById('filter-manual').checked;
            
            var filtered = allData.filter(function(item) {{
                var roundMatch = item.회차 >= minRound && item.회차 <= maxRound;
                var methodMatch = (showAuto && item.당첨방식 === '자동') || 
                                 (showManual && item.당첨방식 === '수동');
                return roundMatch && methodMatch;
            }});
            
            document.getElementById('filtered-count').textContent = filtered.length;
            alert('필터가 적용되었습니다! ' + filtered.length + '건의 데이터가 선택되었습니다.');
        }});
    </script>
    """
    
    m.get_root().html.add_child(folium.Element(filter_html))
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    # Save map
    m.save(output_file)
    print(f"\n✅ Map saved to {output_file}")
    print(f"📊 Total markers: {len(geocoded_df)}")
    print(f"🎯 Total records: {len(df)}")
    
    return output_file

if __name__ == "__main__":
    output = create_interactive_map()
    print(f"\n🎉 Success! Open {output} in your browser to view the interactive map.")
