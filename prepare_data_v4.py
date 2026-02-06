import pandas as pd
import requests
import json
import time
from pathlib import Path

# --- CONFIGURATION ---
REST_API_KEY = "d70d1805bba48840393cec5aa84bca53"
INPUT_FILE = "temp_data.xlsx" # Healthy original data
OUTPUT_JSON = "lotto_data.json"
CACHE_FILE = "geocoded_cache_healthy.xlsx" # New cache to avoid corruption

def get_kakao_geocode(address):
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": f"KakaoAK {REST_API_KEY}"}
    params = {"query": address}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data['documents']:
                node = data['documents'][0]
                return float(node['y']), float(node['x'])
    except: pass
    return None, None

def main():
    print("Regenerating lotto data from healthy source...")
    
    # 1. Load Healthy Data
    df = pd.read_excel(INPUT_FILE)
    # Map columns correctly
    df = df.rename(columns={
        df.columns[0]: 'r', # Round
        df.columns[2]: 'n', # Name
        df.columns[3]: 'm', # Method
        df.columns[4]: 'a'  # Address
    })
    
    # 2. Extract Unique Addresses
    unique_shops = df.groupby(['n', 'a']).size().reset_index()
    total_shops = len(unique_shops)
    print(f"Total unique shops: {total_shops}")

    # 3. Load Cache (if any)
    cache = {}
    if Path(CACHE_FILE).exists():
        cache_df = pd.read_excel(CACHE_FILE)
        cache = {row['a']: (row['lat'], row['lng']) for _, row in cache_df.iterrows()}
        print(f"Loaded {len(cache)} cached locations.")

    # 4. Geocode Missing
    print("Geocoding unique shops (5% increment tracking)...")
    new_geocodes = 0
    last_reported_pct = -1
    
    for idx, row in unique_shops.iterrows():
        name = row['n']
        addr = row['a']
        
        if addr not in cache:
            # Clean address for API
            clean_addr = addr.split(" 1층")[0].split("지하")[0].strip()
            lat, lng = get_kakao_geocode(clean_addr)
            if lat and lng:
                cache[addr] = (lat, lng)
                new_geocodes += 1
                
                # Check percentage (of total unique shops)
                current_total_geocoded = len(cache)
                pct = int((current_total_geocoded / total_shops) * 100)
                if pct % 5 == 0 and pct != last_reported_pct:
                    print(f"PROGRESS_ALERT: {pct}% complete ({current_total_geocoded}/{total_shops})", flush=True)
                    last_reported_pct = pct

                if new_geocodes % 50 == 0:
                    # Save intermediate cache
                    pd.DataFrame([{'a': k, 'lat': v[0], 'lng': v[1]} for k, v in cache.items()]).to_excel(CACHE_FILE, index=False)
                time.sleep(0.01) # Very fast
            
    print(f"Geocoding complete. Total in cache: {len(cache)}", flush=True)
    
    # Final Cache Save
    pd.DataFrame([{'a': k, 'lat': v[0], 'lng': v[1]} for k, v in cache.items()]).to_excel(CACHE_FILE, index=False)

    # 5. Build Final JSON
    json_data = []
    for _, row in df.iterrows():
        addr = row['a']
        if addr in cache:
            lat, lng = cache[addr]
            json_data.append({
                'r': int(row['r']),
                'n': row['n'],
                'a': row['a'],
                'm': row['m'],
                'lat': lat,
                'lng': lng
            })
            
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    
    print(f"Success! Exported {len(json_data)} records to {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
