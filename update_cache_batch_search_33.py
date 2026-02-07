import json
import os
import pandas as pd

# VERIFIED data for rounds 320-339
verified_data_raw = """
320회 | 16, 19, 23, 25, 41, 45
321회 | 12, 18, 20, 21, 25, 34
322회 | 9, 18, 29, 32, 38, 43
323회 | 10, 14, 15, 32, 36, 42
324회 | 2, 4, 21, 25, 33, 36
325회 | 7, 17, 20, 32, 44, 45
326회 | 16, 23, 25, 33, 36, 39
327회 | 6, 12, 13, 17, 32, 44
328회 | 1, 6, 9, 16, 17, 28
329회 | 9, 17, 19, 30, 35, 42
330회 | 3, 4, 16, 17, 19, 20
331회 | 4, 9, 14, 26, 31, 44
332회 | 16, 17, 34, 36, 42, 45
333회 | 5, 14, 27, 30, 39, 43
334회 | 13, 15, 21, 29, 39, 43
335회 | 5, 9, 16, 23, 26, 45
336회 | 3, 5, 20, 34, 35, 44
337회 | 1, 5, 14, 18, 32, 37
338회 | 2, 13, 34, 38, 42, 45
339회 | 6, 8, 14, 21, 30, 37
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
