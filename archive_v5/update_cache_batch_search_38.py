import json
import os
import pandas as pd

# VERIFIED data for rounds 220-239
verified_data_raw = """
220회 | 5, 11, 19, 21, 34, 43, 31
221회 | 2, 20, 33, 35, 37, 40, 16
222회 | 5, 7, 28, 29, 39, 43, 22
223회 | 1, 3, 18, 20, 26, 27, 14
224회 | 4, 19, 26, 27, 30, 42, 31
225회 | 5, 11, 13, 19, 31, 36, 4
226회 | 2, 6, 8, 14, 21, 22, 20
227회 | 4, 5, 15, 16, 22, 42, 34
228회 | 17, 25, 35, 36, 39, 44, 19
229회 | 4, 5, 9, 11, 23, 38, 20
230회 | 5, 11, 14, 29, 32, 33, 18
231회 | 5, 10, 19, 31, 44, 45, 38
232회 | 8, 9, 10, 12, 24, 44, 23
233회 | 4, 6, 13, 17, 28, 40, 3
234회 | 1, 2, 18, 20, 26, 43, 29
235회 | 10, 22, 24, 25, 30, 43, 32
236회 | 1, 4, 8, 13, 37, 39, 7
237회 | 2, 12, 17, 19, 28, 42, 29
238회 | 2, 4, 15, 28, 31, 34, 35
239회 | 11, 15, 24, 39, 41, 44, 4
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
