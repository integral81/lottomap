import requests
import json
import os
import time
import random
import pandas as pd

CACHE_FILE = "lotto_fetch_cache.json"
TEMP_CSV = "lotto_history_backups.csv"

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def save_to_csv_backup(cache):
    if not cache:
        return
    df = pd.DataFrame(list(cache.values()))
    df = df.sort_values(by="회차", ascending=False)
    df.to_csv(TEMP_CSV, index=False, encoding="utf-8-sig")
    print(f"[*] Backup saved to {TEMP_CSV}")

def fetch_10_rounds(batch_size=10):
    cache = load_cache()
    fetched_this_batch = 0
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }
    
    all_rounds = list(range(1, 1210))
    missing_rounds = [r for r in all_rounds if str(r) not in cache]
    missing_rounds.sort(reverse=True) # Start from newest missing
    
    if not missing_rounds:
        print("[!] All rounds are already in cache.")
        return 0

    print(f"[*] Total rounds missing: {len(missing_rounds)}")
    print(f"[*] Starting fetch for next {min(batch_size, len(missing_rounds))} rounds with safety delays...")

    for drw_no in missing_rounds:
        if fetched_this_batch >= batch_size:
            break
            
        url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={drw_no}"
        
        try:
            # 10개씩 더 천천히 (2.0~4.0초 지연)
            time.sleep(random.uniform(2.0, 4.0))
            
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
                    fetched_this_batch += 1
                    print(f"[{fetched_this_batch}/{batch_size}] Round {drw_no} success.")
                else:
                    print(f"[FAIL] Round {drw_no}: Invalid API/No data.")
            elif res.status_code == 403:
                print(f"[ALERT] Round {drw_no}: 403 Forbidden. Throttling detected.")
                break
            else:
                print(f"[ERR] Round {drw_no}: Status {res.status_code}")
                time.sleep(30) # Heavy wait on block
                
        except Exception as e:
            print(f"[EXC] Round {drw_no}: {str(e)}")
            time.sleep(10)

    # 10회차가 끝날 때마다 중간 저장
    save_cache(cache)
    save_to_csv_backup(cache)
    
    return fetched_this_batch

if __name__ == "__main__":
    fetch_10_rounds()
