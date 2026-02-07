import json
import os
import pandas as pd

# VERIFIED data for rounds 300-319
verified_data_raw = """
300회 | 7, 9, 10, 12, 26, 38, 39
301회 | 7, 11, 13, 33, 37, 43, 26
302회 | 9, 15, 17, 24, 30, 39, 12
303회 | 2, 14, 17, 30, 38, 45, 43
304회 | 4, 10, 16, 26, 33, 41, 38
305회 | 7, 8, 18, 21, 23, 39, 9
306회 | 4, 18, 23, 30, 34, 41, 19
307회 | 5, 15, 21, 23, 25, 45, 12
308회 | 14, 15, 17, 19, 37, 45, 40
309회 | 1, 2, 5, 11, 18, 36, 22
310회 | 1, 5, 19, 28, 34, 41, 16
311회 | 4, 12, 24, 27, 28, 32, 10
312회 | 2, 3, 5, 6, 12, 20, 25
313회 | 9, 17, 34, 35, 43, 45, 2
314회 | 15, 17, 19, 34, 38, 41, 2
315회 | 1, 13, 33, 35, 43, 45, 23
316회 | 10, 11, 21, 27, 31, 39, 43
317회 | 3, 10, 11, 22, 36, 39, 8
318회 | 2, 17, 19, 20, 34, 45, 21
319회 | 5, 8, 22, 28, 33, 42, 37
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
