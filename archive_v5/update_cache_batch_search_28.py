import json
import os
import pandas as pd

# VERIFIED data for rounds 420-439
verified_data_raw = """
420회 | 4, 9, 10, 29, 31, 34
421회 | 6, 11, 26, 27, 28, 44
422회 | 8, 15, 19, 21, 34, 44
423회 | 1, 17, 27, 28, 29, 40
424회 | 10, 11, 26, 31, 34, 44
425회 | 8, 10, 14, 27, 33, 38
426회 | 4, 17, 18, 27, 39, 43
427회 | 6, 7, 15, 24, 28, 30
428회 | 12, 16, 19, 22, 37, 40
429회 | 3, 23, 28, 34, 39, 42
430회 | 1, 3, 16, 18, 30, 34
431회 | 18, 22, 25, 31, 38, 45
432회 | 2, 3, 5, 11, 27, 39
433회 | 19, 23, 29, 33, 35, 43
434회 | 3, 13, 20, 24, 33, 37
435회 | 8, 16, 26, 30, 38, 45
436회 | 9, 14, 20, 22, 33, 34
437회 | 11, 16, 29, 38, 41, 44
438회 | 6, 12, 20, 26, 29, 38
439회 | 1, 8, 14, 18, 30, 42
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
