import pandas as pd
import json
import os

CACHE_FILE = "lotto_fetch_cache.json"
FINAL_FILE = "lotto_historic_numbers_1_1209_Final.xlsx"

def sync_excel_to_cache():
    if not os.path.exists(FINAL_FILE):
        print(f"[!] {FINAL_FILE} not found.")
        return

    df = pd.read_excel(FINAL_FILE)
    
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            cache = json.load(f)
    else:
        cache = {}

    count = 0
    for _, row in df.iterrows():
        drw_no = str(int(row['회차']))
        if drw_no not in cache:
            cache[drw_no] = {
                '회차': int(row['회차']),
                '추첨일': str(row['추첨일']),
                '번호1': int(row['번호1']),
                '번호2': int(row['번호2']),
                '번호3': int(row['번호3']),
                '번호4': int(row['번호4']),
                '번호5': int(row['번호5']),
                '번호6': int(row['번호6'])
            }
            count += 1
    
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)
    
    print(f"Synced {count} rounds from Excel to cache. Total in cache: {len(cache)}")

if __name__ == "__main__":
    sync_excel_to_cache()
