import json
import os
import pandas as pd

# VERIFIED data for rounds 640-659
verified_data_raw = """
640회 | 14, 15, 18, 21, 26, 35
641회 | 11, 18, 21, 36, 37, 43
642회 | 8, 17, 18, 24, 39, 45
643회 | 15, 24, 31, 32, 33, 40
644회 | 5, 13, 17, 23, 28, 36
645회 | 1, 4, 16, 26, 40, 41
646회 | 2, 9, 24, 41, 43, 45
647회 | 5, 16, 21, 23, 24, 30
648회 | 13, 19, 28, 37, 38, 43
649회 | 3, 21, 22, 33, 41, 42
650회 | 3, 4, 7, 11, 31, 41
651회 | 11, 12, 16, 26, 29, 44
652회 | 3, 13, 15, 40, 41, 44
653회 | 5, 6, 26, 27, 38, 39
654회 | 16, 21, 26, 31, 36, 43
655회 | 7, 37, 38, 39, 40, 44
656회 | 3, 7, 14, 16, 31, 40
657회 | 10, 14, 19, 39, 40, 43
658회 | 8, 19, 25, 28, 32, 36
659회 | 7, 18, 19, 27, 29, 42
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
