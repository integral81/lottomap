import json
import os
import pandas as pd

# VERIFIED data for rounds 720-739
verified_data_raw = """
720회 | 1, 10, 11, 21, 32, 45
721회 | 1, 28, 35, 41, 43, 44
722회 | 12, 14, 21, 30, 39, 43
723회 | 20, 30, 33, 35, 36, 44
724회 | 2, 8, 33, 35, 37, 41
725회 | 6, 7, 19, 21, 41, 43
726회 | 1, 11, 21, 23, 34, 44
727회 | 7, 8, 10, 19, 21, 31
728회 | 3, 6, 10, 30, 34, 37
729회 | 11, 17, 21, 26, 36, 45
730회 | 4, 10, 14, 15, 18, 22
731회 | 2, 7, 13, 25, 42, 45
732회 | 2, 4, 5, 17, 27, 32
733회 | 11, 24, 32, 33, 35, 40
734회 | 6, 16, 37, 38, 41, 45
735회 | 5, 10, 13, 27, 37, 41
736회 | 2, 11, 17, 18, 21, 27
737회 | 13, 15, 18, 24, 27, 41
738회 | 23, 27, 28, 38, 42, 43
739회 | 7, 22, 29, 33, 34, 35
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
