
import json
import requests
import time
import collections
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import os

# Configuration
KAKAO_API_KEY = "84b62e85ed3ec32fca558717eda26006" # REST API Key
HEADERS = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
INPUT_FILE = "shops_to_verify_all.json"
OUTPUT_FILE = "verification_results_all.json"
MAX_WORKERS = 10 

# Thread-safe results and progress
results = []
results_lock = threading.Lock()
processed_keys = set()

def load_existing_results():
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                global results, processed_keys
                results = data
                for entry in data:
                    shop = entry['original']
                    key = f"{shop['n']}|{shop['a']}"
                    processed_keys.add(key)
                print(f"Resuming from {len(results)} existing results.")
        except Exception as e:
            print(f"Error loading existing results: {e}. Starting fresh.")

def save_current_results():
    with results_lock:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

def search_place(query, lat=None, lng=None):
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    params = {"query": query, "size": 5}
    if lat and lng:
        params['y'] = lat
        params['x'] = lng
        params['radius'] = 1000
    
    try:
        resp = requests.get(url, headers=HEADERS, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json().get('documents', [])
    except Exception:
        return []

def normalize_addr(addr):
    if not addr: return ""
    return addr.replace('경기', '').replace('서울', '').replace('부산', '').replace('대구', '').replace('인천', '').replace('광주', '').replace('대전', '').replace('울산', '').replace('세종', '').replace('강원', '').replace('충북', '').replace('충남', '').replace('전북', '').replace('전남', '').replace('경북', '').replace('경남', '').replace('제주', '').replace(' ', '')

def process_single_shop(shop, total_count):
    name = shop['n']
    addr = shop['a']
    key = f"{name}|{addr}"
    
    if key in processed_keys:
        return

    search_res = search_place(name)
    status = "UNKNOWN"
    match_details = None
    found_exact = False
    found_similar = []
    norm_addr = normalize_addr(addr)
    
    for item in search_res:
        item_addr = item.get('road_address_name') or item.get('address_name')
        item_name = item.get('place_name')
        norm_item_addr = normalize_addr(item_addr)
        
        if name.replace(' ', '') in item_name.replace(' ', '') and norm_addr[:5] in norm_item_addr:
            found_exact = True
            status = "CONFIRMED"
            match_details = item
            break
        if norm_addr[:5] in norm_item_addr:
            found_similar.append(item)
            
    if not found_exact:
        addr_res = search_place(addr)
        if addr_res:
            for item in addr_res:
                if any(x in item.get('category_name', '') for x in ['복권', '편의점']) or '가판' in item.get('place_name', ''):
                    status = "RENAMED_OR_MOVED"
                    match_details = item
                    break
            if status == "UNKNOWN": 
                status = "ADDRESS_EXISTS_BUT_NO_SHOP"
        else:
            if not found_similar:
                status = "NOT_FOUND"
            else:
                status = "AMBIGUOUS"
                match_details = found_similar[0]

    res_entry = {
        "original": shop,
        "status": status,
        "api_result": match_details,
        "candidates": len(search_res)
    }
    
    with results_lock:
        results.append(res_entry)
        count = len(results)
        if count % 50 == 0 or count == total_count:
            percent = (count / total_count) * 100
            print(f"Progress: {count}/{total_count} ({percent:.1f}%)", flush=True)
            # Periodic save to disk
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)

def verify_shops_parallel():
    load_existing_results()
    
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            shops = json.load(f)
    except FileNotFoundError:
        print(f"Input file {INPUT_FILE} not found.")
        return

    total = len(shops)
    print(f"Verifying {total} shops with {MAX_WORKERS} workers...", flush=True)
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(process_single_shop, shop, total) for shop in shops]
        for future in as_completed(futures):
            pass
            
    # Final save
    save_current_results()
    print("\nVerification Complete!", flush=True)

if __name__ == "__main__":
    verify_shops_parallel()
