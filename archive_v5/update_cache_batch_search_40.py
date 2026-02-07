import json
import os
import pandas as pd

# VERIFIED data for rounds 180-199
verified_data_raw = """
180회 | 2, 15, 20, 21, 29, 34, 22
181회 | 14, 21, 23, 32, 40, 45, 44
182회 | 13, 15, 27, 29, 34, 40, 35
183회 | 2, 18, 24, 34, 40, 42, 5
184회 | 1, 2, 6, 16, 20, 33, 41
185회 | 1, 2, 4, 8, 19, 38, 14
186회 | 1, 3, 10, 18, 22, 28, 27
187회 | 1, 2, 8, 18, 29, 38, 42
188회 | 19, 24, 27, 30, 31, 34, 36
189회 | 8, 14, 32, 35, 37, 45, 28
190회 | 1, 10, 19, 21, 23, 44, 18
191회 | 5, 6, 24, 25, 32, 37, 8
192회 | 1, 3, 10, 16, 26, 42, 30
193회 | 6, 14, 18, 26, 36, 39, 13
194회 | 15, 20, 23, 26, 39, 44, 28
195회 | 7, 10, 19, 22, 35, 40, 31
196회 | 35, 36, 37, 41, 44, 45, 30
197회 | 7, 12, 16, 34, 42, 45, 4
198회 | 12, 19, 20, 25, 41, 45, 2
199회 | 14, 21, 22, 25, 30, 36, 43
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
