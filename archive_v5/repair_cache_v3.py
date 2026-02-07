import pandas as pd
import requests
import os
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys

# --- CONFIGURATION ---
CACHE_FILE = "geocoded_cache_healthy.xlsx"
KAKAO_API_KEY = "d70d1805bba48840393cec5aa84bca53"
MAX_WORKERS = 10 # Parallel requests

def geocode(address, api_key):
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": f"KakaoAK {api_key}"}
    params = {"query": address}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        data = response.json()
        if data.get('documents'):
            pos = data['documents'][0]
            return address, float(pos['y']), float(pos['x'])
    except Exception as e:
        pass
    return address, None, None

def main():
    if not Path(CACHE_FILE).exists():
        print(f"Error: {CACHE_FILE} not found.", flush=True)
        return

    print(f"Loading {CACHE_FILE}...", flush=True)
    df = pd.read_excel(CACHE_FILE)
    
    dup_groups = df.groupby(['lat', 'lng'])
    problematic_addresses = []

    for coords, group in dup_groups:
        if len(group) > 1:
            group['city'] = group['a'].str.split().str[0]
            if group['city'].nunique() > 1 or group['a'].nunique() > 1:
                problematic_addresses.extend(group['a'].tolist())

    problematic_addresses = list(set(problematic_addresses))
    total_to_repair = len(problematic_addresses)
    print(f"Total problematic addresses to repair: {total_to_repair}", flush=True)

    if total_to_repair == 0:
        print("Everything looks clean! No repairs needed.", flush=True)
        return

    print(f"Starting PARALLEL re-geocoding (Workers: {MAX_WORKERS})...", flush=True)
    
    results = {}
    completed = 0
    milestone_step = max(1, total_to_repair // 10)
    last_milestone = 0

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_addr = {executor.submit(geocode, addr, KAKAO_API_KEY): addr for addr in problematic_addresses}
        
        for future in as_completed(future_to_addr):
            addr, lat, lng = future.result()
            if lat and lng:
                results[addr] = (lat, lng)
            
            completed += 1
            if completed % 100 == 0 or completed == total_to_repair:
                print(f"  [Progress] {completed}/{total_to_repair} ({(completed/total_to_repair*100):.1f}%)", flush=True)
            
            # Milestone logic for reporting
            current_milestone = completed // milestone_step
            if current_milestone > last_milestone:
                last_milestone = current_milestone
                print(f"MILESTONE_REACHED: {current_milestone * 10}%", flush=True)

    # 3. Apply results and Save
    print("Applying updates to dataframe...", flush=True)
    for addr, (lat, lng) in results.items():
        df.loc[df['a'] == addr, 'lat'] = lat
        df.loc[df['a'] == addr, 'lng'] = lng

    if 'city' in df.columns:
        df = df.drop(columns=['city'])
        
    df.to_excel(CACHE_FILE, index=False)
    print(f"Finished! Successfully updated {len(results)} addresses.", flush=True)

if __name__ == "__main__":
    main()
