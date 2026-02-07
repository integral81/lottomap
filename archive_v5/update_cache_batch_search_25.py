import json
import os
import pandas as pd

# VERIFIED data for rounds 500-519
verified_data_raw = """
500회 | 3, 4, 12, 20, 24, 34
501회 | 6, 8, 14, 28, 38, 41
502회 | 5, 7, 10, 11, 28, 45
503회 | 1, 5, 27, 30, 34, 36
504회 | 5, 10, 11, 14, 21, 26
505회 | 7, 20, 22, 25, 38, 40
506회 | 6, 9, 11, 22, 24, 30
507회 | 12, 13, 32, 33, 40, 41
508회 | 5, 27, 31, 34, 35, 43
509회 | 12, 25, 29, 35, 42, 43
510회 | 12, 29, 32, 33, 39, 40
511회 | 4, 12, 18, 20, 26, 44
512회 | 4, 5, 9, 13, 26, 27
513회 | 7, 16, 17, 26, 30, 36
514회 | 2, 7, 10, 25, 36, 44
515회 | 2, 11, 12, 15, 23, 37
516회 | 1, 11, 14, 22, 30, 31
517회 | 1, 9, 12, 28, 36, 41
518회 | 4, 15, 17, 28, 35, 39
519회 | 6, 8, 13, 16, 30, 43
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
