import json
import os
import pandas as pd

# VERIFIED data for rounds 240-259
verified_data_raw = """
240회 | 1, 8, 11, 23, 27, 42
241회 | 4, 19, 20, 21, 32, 34
242회 | 1, 10, 15, 17, 24, 30, 26
243회 | 2, 12, 17, 19, 28, 42, 34
244회 | 13, 16, 25, 36, 37, 38
245회 | 9, 11, 27, 31, 32, 38
246회 | 13, 18, 21, 23, 26, 39, 15
247회 | 12, 15, 28, 36, 39, 40, 13
248회 | 3, 8, 17, 23, 38, 45, 13
249회 | 3, 8, 27, 31, 41, 44, 11
250회 | 19, 23, 30, 37, 43, 45, 38
251회 | 6, 7, 19, 25, 28, 38, 45
252회 | 14, 23, 26, 31, 39, 45, 28
253회 | 8, 19, 25, 31, 34, 36, 33
254회 | 1, 5, 19, 20, 24, 30, 27
255회 | 1, 5, 6, 24, 27, 42, 32
256회 | 4, 11, 14, 21, 23, 43, 32
257회 | 6, 13, 27, 31, 32, 37, 4
258회 | 3, 10, 11, 20, 31, 40, 28
259회 | 4, 5, 14, 35, 42, 45, 34
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
