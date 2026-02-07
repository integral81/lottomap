import json
import os
import pandas as pd

# VERIFIED data for rounds 480-499
verified_data_raw = """
480회 | 3, 5, 10, 17, 30, 31
481회 | 3, 4, 23, 29, 40, 41
482회 | 1, 10, 16, 24, 25, 35
483회 | 12, 15, 19, 22, 28, 34
484회 | 1, 3, 27, 28, 32, 45
485회 | 17, 22, 26, 27, 36, 39
486회 | 1, 2, 23, 25, 38, 40
487회 | 4, 8, 25, 27, 37, 41
488회 | 2, 8, 17, 30, 31, 38
489회 | 2, 4, 8, 15, 20, 27
490회 | 2, 7, 26, 29, 40, 43
491회 | 8, 17, 35, 36, 39, 42
492회 | 22, 27, 31, 35, 37, 40
493회 | 20, 22, 26, 33, 36, 37
494회 | 5, 7, 8, 15, 30, 43
495회 | 4, 13, 22, 27, 34, 44
496회 | 4, 13, 20, 29, 36, 41
497회 | 19, 20, 23, 24, 43, 44
498회 | 13, 14, 24, 32, 39, 41
499회 | 5, 20, 23, 27, 35, 40
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
