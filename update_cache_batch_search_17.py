import json
import os
import pandas as pd

# VERIFIED data for rounds 660-679
verified_data_raw = """
660회 | 4, 9, 23, 33, 39, 44
661회 | 2, 3, 12, 20, 27, 38
662회 | 5, 6, 9, 11, 15, 37
663회 | 3, 5, 8, 19, 38, 42
664회 | 10, 20, 33, 36, 41, 44
665회 | 5, 6, 11, 17, 38, 44
666회 | 2, 4, 6, 11, 17, 28
667회 | 15, 17, 25, 37, 42, 43
668회 | 12, 14, 15, 24, 27, 32
669회 | 7, 8, 20, 29, 33, 38
670회 | 11, 18, 26, 27, 40, 41
671회 | 7, 9, 10, 13, 31, 35
672회 | 8, 21, 28, 31, 36, 45
673회 | 7, 10, 17, 29, 33, 44
674회 | 9, 10, 14, 25, 27, 31
675회 | 1, 8, 11, 15, 18, 45
676회 | 1, 8, 17, 34, 39, 45
677회 | 12, 15, 24, 36, 41, 44
678회 | 4, 5, 6, 12, 25, 37
679회 | 3, 5, 7, 14, 26, 34
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
