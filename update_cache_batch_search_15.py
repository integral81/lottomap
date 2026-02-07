import json
import os
import pandas as pd

# VERIFIED data for rounds 700-719
verified_data_raw = """
700회 | 11, 23, 28, 29, 30, 44
701회 | 6, 9, 13, 23, 24, 29
702회 | 1, 10, 16, 17, 24, 30
703회 | 7, 8, 14, 27, 34, 36
704회 | 1, 13, 20, 25, 34, 43
705회 | 3, 12, 16, 23, 29, 30
706회 | 1, 17, 26, 32, 40, 44
707회 | 6, 10, 26, 30, 32, 43
708회 | 1, 5, 6, 21, 35, 43
709회 | 1, 12, 19, 21, 37, 43
710회 | 13, 18, 20, 21, 35, 38
711회 | 4, 15, 23, 25, 27, 33
712회 | 2, 8, 16, 17, 22, 33
713회 | 4, 11, 15, 24, 28, 44
714회 | 2, 10, 12, 23, 33, 40
715회 | 4, 14, 15, 21, 29, 34
716회 | 10, 12, 13, 20, 29, 36
717회 | 1, 5, 11, 23, 28, 44
718회 | 1, 10, 11, 15, 23, 43
719회 | 4, 8, 13, 19, 20, 43
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
