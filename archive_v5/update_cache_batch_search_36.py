import json
import os
import pandas as pd

# VERIFIED data for rounds 260-279
verified_data_raw = """
260회 | 1, 10, 11, 16, 32, 45, 40
261회 | 6, 11, 16, 18, 31, 43, 2
262회 | 9, 12, 24, 25, 29, 31, 36
263회 | 3, 4, 18, 23, 33, 45, 29
264회 | 9, 16, 27, 36, 41, 44, 5
265회 | 7, 15, 23, 24, 30, 38, 18
266회 | 8, 11, 13, 20, 27, 39, 42
267회 | 2, 7, 21, 27, 31, 37, 16
268회 | 1, 9, 13, 21, 33, 37, 30
269회 | 5, 18, 20, 36, 42, 43, 32
270회 | 1, 13, 22, 28, 33, 45, 43
271회 | 3, 8, 9, 27, 29, 40, 36
272회 | 1, 12, 19, 23, 30, 44, 4
273회 | 9, 10, 19, 32, 33, 40, 14
274회 | 4, 11, 12, 28, 31, 35, 17
275회 | 2, 6, 21, 27, 34, 43, 19
276회 | 1, 4, 15, 16, 28, 43, 34
277회 | 1, 7, 10, 24, 27, 36, 39
278회 | 1, 3, 20, 25, 30, 42, 23
279회 | 7, 8, 12, 27, 34, 38, 33
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
