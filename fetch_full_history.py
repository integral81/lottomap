import requests
import pandas as pd
import time
import json
import os

CACHE_FILE = "lotto_fetch_cache.json"

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def fetch_all_rounds(start_round, end_round):
    cache = load_cache()
    results = []
    total_to_fetch = end_round - start_round + 1
    fetched_count = 0
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }
    
    # Milestones (10% increments)
    milestones = [int(total_to_fetch * i / 10) for i in range(1, 11)]
    
    print(f"[*] Starting fetch for rounds {end_round} down to {start_round}...")
    
    for drw_no in range(end_round, start_round - 1, -1):
        if str(drw_no) in cache:
            results.append(cache[str(drw_no)])
            fetched_count += 1
        else:
            url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={drw_no}"
            retries = 3
            success = False
            while retries > 0 and not success:
                try:
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
                            results.append(item)
                            cache[str(drw_no)] = item
                            save_cache(cache)
                            fetched_count += 1
                            success = True
                        else:
                            print(f"[FAIL] Round {drw_no} failed.")
                            break
                    else:
                        print(f"[ERR] Round {drw_no} status {res.status_code}")
                        retries -= 1
                        time.sleep(2)
                except Exception as e:
                    print(f"[EXC] Round {drw_no}: {str(e)}")
                    retries -= 1
                    time.sleep(2)
            
            if not success:
                print(f"[CRIT] Could not fetch round {drw_no} after retries.")
            
            # Progress check
            if fetched_count in milestones:
                percent = (milestones.index(fetched_count) + 1) * 10
                print(f"\n[PROGRESS] {percent}% completed ({fetched_count}/{total_to_fetch} rounds fetched)\n")
            
            # Delay to avoid blocking
            time.sleep(1.2)
            
    return results

if __name__ == "__main__":
    # Target rounds 1 to 1159
    all_results = fetch_all_rounds(1, 1159)
    
    # Load 1160-1209 data from the previous Final file if it exists
    final_file = "lotto_historic_numbers_1_1209_Final.xlsx"
    if os.path.exists(final_file):
        df_prev = pd.read_excel(final_file)
        # Convert to list of dicts
        prev_results = df_prev.to_dict('records')
        # Combine and remove duplicates based on '회차'
        combined = {item['회차']: item for item in all_results + prev_results}
        final_list = list(combined.values())
    else:
        final_list = all_results
        
    df_final = pd.DataFrame(final_list)
    df_final = df_final.sort_values(by='회차', ascending=False)
    df_final.to_excel(final_file, index=False)
    print(f"\n[FINISH] All 1209 rounds saved to {final_file}")
