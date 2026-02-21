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
HISTORIC_FILE = "lotto_historic_numbers_1_1209_Final.xlsx"
KAKAO_API_KEY = os.environ.get("KAKAO_REST_API_KEY") # Set this in GitHub Secrets

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Referer': 'https://www.dhlottery.co.kr/',
}

def normalize_address(addr):
    if not isinstance(addr, str): return addr
    addr = addr.strip()
    addr = re.sub(r'(\d+)번�?', r'\1', addr)
    addr = re.sub(r'(\d+-\d+)번�?', r'\1', addr)
    addr = re.sub(r'\s(\d+)�?', '', addr)
    addr = re.sub(r'\s지??s*(\d*)�?$', '', addr)
    addr = addr.rstrip('., ')
    if addr.endswith('번�?'): addr = addr[:-2].strip()
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
        response = requests.get(url, headers=HEADERS, timeout=15)
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


def scrape_winning_numbers(draw_no):
    print(f"Scraping numbers for round {draw_no}...")
    url = f"https://www.dhlottery.co.kr/gameResult.do?method=byWin765&drwNo={draw_no}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        div_win = soup.find('div', class_='win_result')
        if not div_win: return None
        
        # Numbers are in spans inside <div class="num win">
        num_div = div_win.find('div', class_='num win')
        if not num_div: return None
        
        spans = num_div.find_all('span', class_='ball_645')
        # Expect 6 numbers
        nums = [int(s.get_text()) for s in spans][:6]
        
        # Bonus Number
        bonus_div = div_win.find('div', class_='num bonus')
        if bonus_div:
            bonus_span = bonus_div.find('span', class_='ball_645')
            if bonus_span:
                nums.append(int(bonus_span.get_text()))
                
        return nums
    except Exception as e:
        print(f"Error scraping numbers for {draw_no}: {e}")
        return None

def update_historic_file(draw_no, numbers):
    if not Path(HISTORIC_FILE).exists():
        print(f"{HISTORIC_FILE} not found. Skipping update.")
        return

    try:
        df = pd.read_excel(HISTORIC_FILE)
        # Check if round exists
        if draw_no in df['?�차'].values:
            print(f"Round {draw_no} already in historic file.")
            return
            
        # Create new row
        new_row = {'?�차': draw_no}
        for i, n in enumerate(numbers, 1):
            if i == 7:
                new_row['보너??] = n
            else:
                new_row[f'번호{i}'] = n
            
        # Append
        df = pd.concat([pd.DataFrame([new_row]), df], ignore_index=True)
        # Sort desc
        df = df.sort_values(by='?�차', ascending=False)
        
        df.to_excel(HISTORIC_FILE, index=False)
        print(f"Updated {HISTORIC_FILE} with round {draw_no} numbers: {numbers}")
    except Exception as e:
        print(f"Failed to update historic file: {e}")

def build_history_json():
    OUTPUT_JSON = "lotto_history.json"
    if not Path(HISTORIC_FILE).exists():
        return

    try:
        df = pd.read_excel(HISTORIC_FILE)
        history_map = {}
        for _, row in df.iterrows():
            round_num = int(row['?�차'])
            # Assuming columns like 번호1, 번호2... match the file structure
            numbers = [
                int(row['번호1']), int(row['번호2']), int(row['번호3']), 
                int(row['번호4']), int(row['번호5']), int(row['번호6'])
            ]
            
            # Helper to safely get bonus
            bonus = 0
            if '보너?? in row and pd.notna(row['보너??]):
                 bonus = int(row['보너??])
            elif '번호7' in row and pd.notna(row['번호7']):
                 bonus = int(row['번호7'])
            
            # If we found a bonus (non-zero), append it. 
            # Note: Older rounds might not have bonus recorded in Excel if it was old format?
            # But the user wants consistency.
            if bonus > 0:
                numbers.append(bonus)
                
            history_map[str(round_num)] = numbers
            
        with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
            json.dump(history_map, f, ensure_ascii=False, indent=None)
        print(f"Rebuilt {OUTPUT_JSON}.")
    except Exception as e:
        print(f"Error building JSON: {e}")

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
        res = requests.get("https://www.dhlottery.co.kr/common.do?method=main", headers=HEADERS, timeout=10)
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
        # Update winning numbers history
        nums = scrape_winning_numbers(r)
        if nums:
             update_historic_file(r, nums)

        # Scrape store locations
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
            # Match columns: [?�차, ?�번 (None), ?�호�? 구분, ?�재지]
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

    # Rebuild history JSON for frontend
    build_history_json()

    print(f"Successfully added {len(final_new_records)} new records up to round {current_round}.")

if __name__ == "__main__":
    main()
