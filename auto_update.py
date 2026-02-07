import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import os
import re
from pathlib import Path
import time

# --- CONFIGURATION ---
JSON_FILE = "lotto_data.json"
EXCEL_FILE = "temp_data.xlsx"
CACHE_FILE = "geocoded_cache_healthy.xlsx"
KAKAO_API_KEY = os.environ.get("KAKAO_REST_API_KEY") # Set this in GitHub Secrets

def normalize_address(addr):
    if not isinstance(addr, str): return addr
    addr = addr.strip()
    addr = re.sub(r'(\d+)번지', r'\1', addr)
    addr = re.sub(r'(\d+-\d+)번지', r'\1', addr)
    addr = re.sub(r'\s(\d+)층$', '', addr)
    addr = re.sub(r'\s지하\s*(\d*)층?$', '', addr)
    addr = addr.rstrip('., ')
    if addr.endswith('번지'): addr = addr[:-2].strip()
    return addr

def geocode(address, api_key, cache):
    if address in cache:
        return cache[address]
    
    if not api_key:
        return None, None
        
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": f"KakaoAK {api_key}"}
    params = {"query": address}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        data = response.json()
        if data.get('documents'):
            pos = data['documents'][0]
            lat, lng = float(pos['y']), float(pos['x'])
            cache[address] = (lat, lng)
            return lat, lng
    except Exception as e:
        print(f"Geocoding error for {address}: {e}")
    
    return None, None

def scrape_round(draw_no):
    print(f"Scraping round {draw_no}...")
    url = f"https://www.dhlottery.co.kr/gameResult.do?method=byWin765&drwNo={draw_no}"
    try:
        response = requests.get(url, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # The 1st prize winner table is usually the first table with tbl_data
        table = soup.find('table', {'class': 'tbl_data'})
        if not table:
            print(f"Winner table not found for round {draw_no}.")
            return []
            
        rows = table.find('tbody').find_all('tr')
        records = []
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 4:
                # Structure: [No, Store Name, Method, Address, ...]
                name = cols[1].get_text(strip=True)
                method = cols[2].get_text(strip=True)
                address = cols[3].get_text(strip=True)
                records.append({
                    'r': draw_no,
                    'n': name,
                    'm': method,
                    'a': normalize_address(address)
                })
        return records
    except Exception as e:
        print(f"Scraping error for round {draw_no}: {e}")
        return []

def main():
    # 1. Load existing data to find last round
    if not Path(JSON_FILE).exists():
        print(f"Error: {JSON_FILE} not found.")
        return
        
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        all_data = json.load(f)
    
    last_round = max([d['r'] for d in all_data]) if all_data else 0
    print(f"Last round in data: {last_round}")
    
    # Check current round from Donghaeng Lotto
    try:
        res = requests.get("https://www.dhlottery.co.kr/common.do?method=main", timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        # Find the latest round number in the main page
        latest_text = soup.find('strong', id='lottoDrwNo')
        if latest_text:
            current_round = int(latest_text.get_text())
        else:
            # Fallback if parsing fails - try 1210 if last was 1209
            current_round = last_round + 1
    except:
        current_round = last_round + 1
        
    print(f"Target latest round: {current_round}")
    
    if last_round >= current_round:
        print("Data is already up to date.")
        return

    # 2. Scrape new rounds
    new_records_base = []
    for r in range(last_round + 1, current_round + 1):
        recs = scrape_round(r)
        if recs:
            new_records_base.extend(recs)
        time.sleep(1) # Be polite
        
    if not new_records_base:
        print("No new records found.")
        return

    # 3. Load Cache
    cache = {}
    if Path(CACHE_FILE).exists():
        try:
            cache_df = pd.read_excel(CACHE_FILE)
            cache = {row['a']: (row['lat'], row['lng']) for _, row in cache_df.iterrows()}
        except: pass

    # 4. Geocode new records
    final_new_records = []
    for rec in new_records_base:
        lat, lng = geocode(rec['a'], KAKAO_API_KEY, cache)
        if lat and lng:
            rec['lat'] = lat
            rec['lng'] = lng
            final_new_records.append(rec)
        else:
            print(f"Skipping {rec['n']} - Geocode failed.")

    if not final_new_records:
        print("No new geocoded records to add.")
        return

    # 5. Merge and Save
    # Merge JSON
    # We want latest rounds first
    combined_json = final_new_records + all_data
    combined_json.sort(key=lambda x: x['r'], reverse=True)
    
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(combined_json, f, ensure_ascii=False, indent=2)
    
    # Merge Excel (temp_data.xlsx)
    if Path(EXCEL_FILE).exists():
        try:
            df_old = pd.read_excel(EXCEL_FILE)
            # Match columns: [회차, 순번 (None), 상호명, 구분, 소재지]
            new_df_data = []
            for r in final_new_records:
                new_df_data.append([r['r'], None, r['n'], r['m'], r['a']])
            
            df_new = pd.DataFrame(new_df_data, columns=df_old.columns[:5])
            df_combined = pd.concat([df_new, df_old], ignore_index=True)
            df_combined.to_excel(EXCEL_FILE, index=False)
        except Exception as e:
            print(f"Excel merge failed: {e}")

    # Update Cache File
    if cache:
        new_cache_df = pd.DataFrame([{'a': k, 'lat': v[0], 'lng': v[1]} for k, v in cache.items()])
        new_cache_df.to_excel(CACHE_FILE, index=False)

    print(f"Successfully added {len(final_new_records)} new records up to round {current_round}.")

if __name__ == "__main__":
    main()
