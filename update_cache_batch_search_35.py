import json
import os
import pandas as pd

# VERIFIED data for rounds 280-299
verified_data_raw = """
280회 | 2, 9, 21, 23, 29, 36, 16
281회 | 1, 10, 11, 24, 30, 43, 32
282회 | 5, 6, 11, 18, 30, 42, 33
283회 | 4, 18, 23, 26, 31, 33, 39
284회 | 3, 10, 12, 18, 33, 44, 25
285회 | 3, 4, 7, 16, 21, 40, 36
286회 | 4, 10, 19, 28, 35, 42, 27
287회 | 7, 13, 20, 24, 25, 41, 19
288회 | 1, 12, 17, 28, 35, 44, 34
289회 | 3, 14, 33, 37, 38, 42, 10
290회 | 5, 11, 13, 17, 36, 45, 43
291회 | 3, 10, 21, 26, 35, 45, 14
292회 | 17, 18, 31, 32, 33, 34, 10
293회 | 1, 9, 17, 21, 29, 33, 24
294회 | 6, 9, 14, 21, 31, 39, 19
295회 | 1, 10, 12, 17, 30, 44, 32
296회 | 1, 13, 21, 23, 29, 44, 4
297회 | 2, 7, 26, 29, 30, 45, 18
298회 | 5, 9, 27, 29, 37, 40, 19
299회 | 1, 5, 10, 24, 30, 40, 41
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
