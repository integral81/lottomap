import requests
import json
import os
import time
import random

CACHE_FILE = "lotto_fetch_cache.json"

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def fetch_batch(start_from, max_fetch=50):
    cache = load_cache()
    rounds_fetched = 0
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }
    
    print(f"[*] Starting batch fetch. Target: {max_fetch} rounds starting from {start_from} downwards.")
    
    for drw_no in range(start_from, 0, -1):
        if rounds_fetched >= max_fetch:
            print(f"\n[DONE] Batch limit ({max_fetch}) reached.")
            break
            
        if str(drw_no) in cache:
            continue
            
        url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={drw_no}"
        success = False
        try:
            # Random delay 1-2 sec
            time.sleep(random.uniform(1.0, 2.0))
            
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code == 200:
                data = res.json()
                if data.get("returnValue") == "success":
                    item = {
                        '회차': data['drwNo'],
                        '추첨일': data['drwNoDate'],
                        '번호1': data['drwtNo1'],
                        '번호2': data['drwtNo2'],
                        '번호3': data['drwtNo3'],
                        '번호4': data['drwtNo4'],
                        '번호5': data['drwtNo5'],
                        '번호6': data['drwtNo6']
                    }
                    cache[str(drw_no)] = item
                    save_cache(cache)
                    rounds_fetched += 1
                    print(f"[{rounds_fetched}/{max_fetch}] Round {drw_no} fetched.")
                    success = True
                else:
                    print(f"[FAIL] Round {drw_no} API failure.")
            else:
                print(f"[ERR] Round {drw_no} Status {res.status_code}")
                
        except Exception as e:
            print(f"[EXC] Round {drw_no}: {str(e)}")
            
        if not success:
            # If failed, wait longer
            time.sleep(5)

    total_in_cache = len(cache)
    print(f"\n[*] Batch complete. Total in cache: {total_in_cache}")
    return total_in_cache

if __name__ == "__main__":
    # Load cache to find the latest missing round
    c = load_cache()
    # Find the max round < 1210 that is NOT in cache
    # Currently 1044-1209 are in cache.
    # We want to start from 1043 down.
    start_point = 1043
    while str(start_point) in c and start_point > 0:
        start_point -= 1
    
    if start_point > 0:
        fetch_batch(start_point, max_fetch=50)
    else:
        print("[!] All rounds fetched.")
