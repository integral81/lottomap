import json
import os
import pandas as pd

# VERIFIED data for rounds 80-99
verified_data_raw = """
80회 | 17, 18, 24, 25, 26, 30, 1
81회 | 5, 7, 11, 13, 20, 33, 6
82회 | 1, 2, 3, 14, 27, 42, 39
83회 | 6, 10, 15, 17, 19, 34, 14
84회 | 16, 23, 27, 34, 42, 45, 11
85회 | 6, 8, 13, 23, 31, 36, 21
86회 | 2, 12, 37, 39, 41, 45, 33
87회 | 4, 12, 16, 23, 34, 43, 26
88회 | 1, 17, 20, 24, 30, 41, 27
89회 | 4, 26, 28, 29, 33, 40, 37
90회 | 17, 20, 29, 35, 38, 44, 10
91회 | 1, 21, 24, 26, 29, 42, 27
92회 | 3, 14, 24, 33, 35, 36, 17
93회 | 6, 22, 24, 36, 38, 44, 19
94회 | 2, 15, 17, 22, 28, 34, 37
95회 | 2, 13, 20, 30, 31, 40, 25
96회 | 1, 3, 8, 21, 22, 31, 20
97회 | 6, 7, 14, 15, 20, 36, 3
98회 | 6, 9, 16, 23, 24, 32, 43
99회 | 1, 3, 10, 27, 29, 37, 11
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
