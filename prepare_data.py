import pandas as pd
import requests
import time
import json
from pathlib import Path

# --- CONFIGURATION ---
REST_API_KEY = "d70d1805bba48840393cec5aa84bca53"  # Existing REST Key
INPUT_FILE = "lotto_results_kinov_cleaned.csv"
CACHE_FILE = "geocoded_cache.xlsx"
OUTPUT_JSON = "lotto_data.json"

def get_kakao_geocode(address):
    """Fetch coordinates from Kakao REST API"""
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
        return None, None
    except Exception as e:
        return None, None

def export_json(df, cache, output_path):
    json_data = []
    # Create a lookup for speed
    for _, row in df.iterrows():
        # Map columns based on index if names are corrupted, 
        # but let's try to use original names first
        try:
            addr = row['소재지']
            name = row['상호명']
            round_num = row['회차']
            method = row['당첨방식']
        except:
            # Fallback to positional mapping if column names are messy
            round_num = row.iloc[0]
            name = row.iloc[2]
            method = row.iloc[3]
            addr = row.iloc[4]

        if addr in cache:
            lat, lon = cache[addr]
            json_data.append({
                'r': int(round_num),
                'n': name,
                'a': addr,
                'm': method,
                'lat': lat,
                'lng': lon
            })
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False)

def main():
    print("Starting data preparation with cleaned CSV...")
    
    # 1. Load Data
    try:
        df = pd.read_csv(INPUT_FILE, encoding='utf-8')
    except:
        df = pd.read_csv(INPUT_FILE, encoding='cp949')
    
    print(f"Loaded {len(df)} records from {INPUT_FILE}")

    # Identify columns (handling potential encoding issues in headers)
    # The user mentioned cleaned_address is the best one to use for geocoding
    # Columns: [0:회차, 1:등위, 2:상호명, 3:당첨방식, 4:소재지, 5:cleaned_address]
    
    # 2. Get Unique Addresses for Geocoding
    # We use '소재지' as the primary key for the cache to maintain consistency, 
    # but use 'cleaned_address' for the actual API call.
    
    # Let's normalize column names if they are garbled
    col_map = {
        df.columns[0]: '회차',
        df.columns[2]: '상호명',
        df.columns[3]: '당첨방식',
        df.columns[4]: '소재지',
        df.columns[5]: 'cleaned_address'
    }
    df = df.rename(columns=col_map)
    
    unique_shops = df.groupby(['상호명', '소재지', 'cleaned_address']).size().reset_index().rename(columns={0: 'count'})
    total_to_process = len(unique_shops)
    print(f"Total unique shop-address pairs: {total_to_process}")

    # 3. Load Cache
    cache = {}
    if Path(CACHE_FILE).exists():
        cache_df = pd.read_excel(CACHE_FILE)
        for _, row in cache_df.iterrows():
            cache[row['소재지']] = (row['lat'], row['lon'])
        print(f"Loaded {len(cache)} cached locations.")

    # 4. Geocode Missing
    geocoded_data = []
    new_geocodes = 0
    last_reported_pct = -1
    
    print("Processing geocoding (5% increment tracking)...")
    
    for idx, row in unique_shops.iterrows():
        name = row['상호명']
        address = row['소재지']
        clean_addr = row['cleaned_address']
        
        lat, lon = None, None
        if address in cache:
            lat, lon = cache[address]
        else:
            lat, lon = get_kakao_geocode(clean_addr)
            if lat and lon:
                cache[address] = (lat, lon)
                new_geocodes += 1
                
                # Check percentage
                current_total_geocoded = len(cache)
                pct = int((current_total_geocoded / total_to_process) * 100)
                if pct % 5 == 0 and pct != last_reported_pct:
                    print(f"PROGRESS_ALERT: {pct}% complete ({current_total_geocoded}/{total_to_process})", flush=True)
                    last_reported_pct = pct
                
                # Incremental save every 50 records
                if new_geocodes % 50 == 0:
                    temp_cache_list = [{'소재지': k, 'lat': v[0], 'lon': v[1]} for k, v in cache.items()]
                    pd.DataFrame(temp_cache_list).to_excel(CACHE_FILE, index=False)
                    export_json(df, cache, OUTPUT_JSON)
                
                time.sleep(0.02)
            
        if lat and lon:
            geocoded_data.append({
                'name': name,
                'address': address,
                'lat': lat,
                'lng': lon
            })
            
    print(f"Geocoding complete. Total geocoded shops: {len(geocoded_data)}", flush=True)

    # Final save
    export_json(df, cache, OUTPUT_JSON)
    cache_list = [{'소재지': k, 'lat': v[0], 'lon': v[1]} for k, v in cache.items()]
    pd.DataFrame(cache_list).to_excel(CACHE_FILE, index=False)
    print("Final save complete.", flush=True)

if __name__ == "__main__":
    main()
