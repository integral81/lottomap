import json
import os
import pandas as pd

# VERIFIED data for rounds 620-639
verified_data_raw = """
620회 | 2, 16, 17, 32, 39, 45
621회 | 5, 10, 11, 16, 26, 40
622회 | 9, 15, 16, 21, 28, 34
623회 | 7, 13, 30, 39, 41, 45
624회 | 1, 7, 19, 26, 27, 35
625회 | 3, 6, 7, 20, 21, 39
626회 | 13, 14, 26, 33, 40, 43
627회 | 2, 9, 22, 25, 31, 45
628회 | 1, 7, 12, 15, 23, 42
629회 | 19, 28, 31, 38, 43, 44
630회 | 8, 17, 21, 24, 27, 31
631회 | 1, 2, 4, 23, 31, 34
632회 | 15, 18, 21, 32, 35, 44
633회 | 9, 12, 19, 20, 39, 41
634회 | 4, 10, 11, 12, 20, 27
635회 | 11, 13, 25, 26, 29, 33
636회 | 6, 7, 15, 16, 26, 40
637회 | 3, 16, 22, 37, 38, 44
638회 | 3, 4, 7, 12, 13, 24
639회 | 6, 15, 22, 23, 25, 32
"""

CACHE_FILE = "lotto_fetch_cache.json"
TEMP_CSV = "lotto_history_backups.csv"

def update_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            cache = json.load(f)
    else:
        cache = {}

    lines = verified_data_raw.strip().split("\n")
    for line in lines:
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 2: continue
        
        drw_no_str = parts[0].replace("회", "")
        nums = [int(n.strip()) for n in parts[1].split(",")]
        
        cache[drw_no_str] = {
            '회차': int(drw_no_str),
            '번호1': nums[0],
            '번호2': nums[1],
            '번호3': nums[2],
            '번호4': nums[3],
            '번호5': nums[4],
            '번호6': nums[5]
        }
    
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)
    
    # Also save to CSV
    df = pd.DataFrame(list(cache.values()))
    df = df.sort_values(by="회차", ascending=False)
    df.to_csv(TEMP_CSV, index=False, encoding="utf-8-sig")
    
    print(f"Updated cache with {len(lines)} VERIFIED rounds. Total in cache: {len(cache)}")

if __name__ == "__main__":
    update_cache()
