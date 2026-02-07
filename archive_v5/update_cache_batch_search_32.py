import json
import os
import pandas as pd

# VERIFIED data for rounds 340-362
verified_data_raw = """
340회 | 6, 12, 15, 34, 35, 41
341회 | 1, 8, 19, 34, 39, 43
342회 | 1, 13, 14, 33, 34, 43
343회 | 1, 10, 17, 29, 31, 43
344회 | 1, 2, 15, 28, 34, 45
345회 | 15, 20, 23, 29, 39, 42
346회 | 5, 13, 14, 22, 44, 45
347회 | 3, 8, 13, 27, 32, 42
348회 | 3, 14, 17, 20, 24, 31
349회 | 5, 13, 14, 20, 24, 25
350회 | 1, 8, 18, 24, 29, 33
351회 | 5, 25, 27, 29, 34, 36
352회 | 5, 16, 17, 20, 26, 41
353회 | 11, 16, 19, 22, 29, 36
354회 | 14, 19, 36, 43, 44, 45
355회 | 5, 8, 29, 30, 35, 44
356회 | 2, 8, 14, 25, 29, 45
357회 | 10, 14, 18, 21, 36, 37
358회 | 1, 9, 10, 12, 21, 40
359회 | 1, 10, 19, 20, 24, 40
360회 | 4, 16, 23, 25, 35, 40
361회 | 5, 10, 16, 24, 27, 35
362회 | 2, 3, 22, 27, 30, 40
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
