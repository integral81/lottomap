import json
import os
import pandas as pd

# VERIFIED data for rounds 140-159
verified_data_raw = """
140회 | 3, 13, 17, 18, 19, 28, 8
141회 | 8, 12, 29, 31, 42, 43, 2
142회 | 12, 16, 30, 34, 40, 44, 19
143회 | 26, 27, 28, 42, 43, 45, 8
144회 | 4, 15, 17, 26, 36, 37, 43
145회 | 2, 3, 13, 20, 27, 44, 9
146회 | 2, 19, 27, 35, 41, 42, 25
147회 | 4, 6, 13, 21, 40, 42, 36
148회 | 21, 25, 33, 34, 35, 36, 17
149회 | 2, 11, 21, 34, 41, 42, 27
150회 | 2, 18, 25, 28, 37, 39, 16
151회 | 1, 2, 10, 13, 18, 19, 15
152회 | 1, 5, 13, 26, 29, 34, 43
153회 | 3, 8, 11, 12, 13, 36, 33
154회 | 6, 19, 21, 35, 40, 45, 20
155회 | 16, 19, 20, 32, 33, 41, 4
156회 | 5, 18, 28, 30, 42, 45, 2
157회 | 19, 26, 30, 33, 35, 39, 37
158회 | 4, 9, 13, 18, 21, 34, 7
159회 | 1, 18, 30, 41, 42, 43, 32
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
