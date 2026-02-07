import json
import os
import pandas as pd

# VERIFIED data for rounds 40-59
verified_data_raw = """
40회 | 9, 13, 21, 25, 32, 42, 2
41회 | 13, 20, 23, 35, 38, 43, 34
42회 | 17, 18, 19, 21, 23, 32, 1
43회 | 6, 31, 35, 38, 39, 44, 1
44회 | 3, 11, 21, 30, 38, 45, 39
45회 | 1, 2, 8, 11, 38, 45, 37
46회 | 8, 13, 15, 23, 31, 38, 39
47회 | 14, 17, 26, 31, 36, 45, 27
48회 | 6, 10, 18, 26, 37, 38, 3
49회 | 4, 7, 16, 19, 33, 40, 30
50회 | 2, 10, 12, 15, 22, 44, 1
51회 | 2, 3, 11, 16, 26, 44, 35
52회 | 2, 4, 15, 16, 20, 29, 1
53회 | 7, 8, 14, 32, 33, 39, 42
54회 | 1, 8, 21, 27, 36, 39, 37
55회 | 17, 21, 31, 37, 40, 44, 7
56회 | 10, 14, 30, 31, 33, 37, 19
57회 | 7, 10, 16, 25, 29, 44, 6
58회 | 10, 24, 25, 33, 40, 44, 1
59회 | 6, 29, 36, 39, 41, 45, 13
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
