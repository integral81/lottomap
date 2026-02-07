import json
import os
import pandas as pd

# VERIFIED data for rounds 560-579
verified_data_raw = """
560회 | 1, 4, 20, 23, 29, 45
561회 | 5, 7, 18, 37, 42, 45
562회 | 4, 11, 13, 17, 20, 31
563회 | 5, 10, 16, 17, 31, 32
564회 | 14, 19, 25, 26, 27, 34
565회 | 4, 10, 18, 27, 40, 45
566회 | 4, 5, 6, 25, 26, 43
567회 | 1, 10, 15, 16, 32, 41
568회 | 1, 3, 17, 20, 31, 44
569회 | 3, 6, 13, 23, 24, 35
570회 | 1, 12, 26, 27, 29, 33
571회 | 11, 18, 21, 26, 38, 43
572회 | 3, 13, 18, 33, 37, 45
573회 | 2, 4, 20, 34, 35, 43
574회 | 14, 15, 16, 19, 25, 43
575회 | 2, 8, 20, 30, 33, 34
576회 | 10, 11, 15, 25, 35, 41
577회 | 16, 17, 22, 31, 34, 37
578회 | 5, 12, 14, 32, 34, 42
579회 | 5, 7, 20, 22, 37, 42
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
