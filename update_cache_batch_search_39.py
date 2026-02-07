import json
import os
import pandas as pd

# VERIFIED data for rounds 200-219
verified_data_raw = """
200회 | 5, 6, 13, 14, 17, 20, 7
201회 | 3, 11, 24, 38, 39, 44, 26
202회 | 12, 14, 27, 33, 39, 44, 17
203회 | 1, 3, 11, 24, 30, 32, 7
204회 | 3, 12, 14, 35, 40, 45, 5
205회 | 2, 7, 13, 27, 30, 39, 38
206회 | 1, 2, 3, 15, 20, 25, 43
207회 | 3, 11, 14, 31, 32, 37, 38
208회 | 14, 25, 31, 34, 40, 44, 24
209회 | 2, 7, 18, 20, 24, 33, 37
210회 | 10, 19, 22, 23, 25, 37, 39
211회 | 12, 13, 17, 20, 33, 41, 8
212회 | 11, 12, 18, 21, 31, 38, 8
213회 | 2, 3, 4, 5, 20, 24, 42
214회 | 5, 7, 20, 25, 28, 37, 32
215회 | 2, 3, 7, 15, 43, 44, 4
216회 | 7, 16, 17, 33, 36, 40, 1
217회 | 16, 20, 27, 33, 35, 39, 38
218회 | 1, 8, 14, 18, 29, 44, 20
219회 | 4, 11, 20, 26, 35, 37, 16
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
