import json
import os
import pandas as pd

# VERIFIED data for rounds 100-119
verified_data_raw = """
100회 | 1, 10, 15, 36, 39, 40, 18
101회 | 2, 8, 26, 31, 38, 43, 1
102회 | 2, 3, 14, 21, 23, 33, 44
103회 | 11, 16, 23, 24, 31, 35, 17
104회 | 1, 14, 27, 30, 31, 41, 29
105회 | 1, 4, 21, 22, 29, 39, 23
106회 | 1, 4, 10, 14, 21, 28, 43
107회 | 1, 16, 20, 24, 37, 43, 36
108회 | 3, 14, 20, 21, 34, 45, 29
109회 | 1, 5, 34, 36, 42, 44, 33
110회 | 7, 20, 22, 23, 29, 43, 45
111회 | 1, 7, 16, 20, 31, 32, 19
112회 | 5, 16, 20, 23, 32, 42, 17
113회 | 1, 5, 12, 16, 26, 36, 32
114회 | 11, 14, 19, 26, 28, 41, 2
115회 | 1, 2, 7, 21, 30, 42, 12
116회 | 2, 4, 25, 31, 34, 37, 17
117회 | 5, 10, 22, 34, 36, 44, 35
118회 | 3, 4, 10, 17, 19, 22, 38
119회 | 3, 11, 13, 14, 17, 21, 38
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
