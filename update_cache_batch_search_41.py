import json
import os
import pandas as pd

# VERIFIED data for rounds 160-179
verified_data_raw = """
160회 | 3, 7, 8, 34, 39, 41, 1
161회 | 22, 34, 36, 40, 42, 45, 44
162회 | 1, 5, 21, 25, 38, 41, 24
163회 | 7, 11, 26, 28, 29, 44, 16
164회 | 6, 9, 10, 11, 39, 41, 27
165회 | 5, 13, 18, 19, 22, 42, 31
166회 | 9, 12, 27, 36, 39, 45, 14
167회 | 24, 27, 28, 30, 36, 39, 4
168회 | 3, 10, 31, 40, 42, 43, 30
169회 | 16, 27, 35, 37, 43, 45, 19
170회 | 2, 11, 13, 15, 31, 42, 10
171회 | 4, 16, 25, 29, 34, 35, 1
172회 | 4, 19, 21, 24, 26, 41, 35
173회 | 3, 9, 24, 30, 33, 34, 18
174회 | 13, 14, 18, 22, 35, 39, 16
175회 | 3, 4, 6, 8, 32, 42, 31
176회 | 4, 17, 30, 32, 33, 34, 15
177회 | 1, 10, 13, 16, 37, 43, 6
178회 | 1, 5, 11, 12, 18, 23, 9
179회 | 3, 16, 18, 24, 40, 44, 21
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
