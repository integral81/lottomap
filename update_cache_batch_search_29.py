import json
import os
import pandas as pd

# VERIFIED data for rounds 400-419
verified_data_raw = """
400회 | 9, 21, 27, 34, 41, 43
401회 | 6, 12, 18, 31, 38, 43
402회 | 5, 9, 15, 19, 22, 36
403회 | 10, 14, 22, 24, 28, 37
404회 | 5, 20, 21, 24, 33, 40
405회 | 1, 2, 10, 25, 26, 44
406회 | 7, 12, 21, 24, 27, 36
407회 | 6, 7, 13, 16, 24, 25
408회 | 9, 20, 21, 22, 30, 37
409회 | 6, 9, 21, 31, 32, 40
410회 | 1, 3, 18, 32, 40, 41
411회 | 11, 14, 22, 35, 37, 39
412회 | 4, 7, 39, 41, 42, 45
413회 | 2, 9, 15, 23, 34, 40
414회 | 2, 14, 15, 22, 23, 44
415회 | 7, 17, 20, 26, 30, 40
416회 | 5, 6, 8, 11, 22, 26
417회 | 4, 5, 14, 20, 22, 43
418회 | 11, 13, 15, 26, 28, 34
419회 | 2, 11, 13, 14, 28, 30
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
