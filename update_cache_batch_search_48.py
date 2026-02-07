import json
import os
import pandas as pd

# VERIFIED data for rounds 20-39
verified_data_raw = """
20회 | 10, 14, 18, 20, 23, 30, 41
21회 | 6, 12, 17, 18, 31, 32, 21
22회 | 4, 5, 6, 8, 17, 39, 25
23회 | 5, 13, 17, 18, 33, 42, 44
24회 | 7, 8, 27, 29, 36, 43, 6
25회 | 2, 4, 21, 26, 43, 44, 16
26회 | 4, 5, 7, 18, 20, 25, 31
27회 | 1, 20, 26, 28, 37, 43, 27
28회 | 9, 18, 23, 25, 35, 37, 1
29회 | 1, 5, 13, 34, 39, 40, 11
30회 | 8, 17, 20, 35, 36, 44, 4
31회 | 7, 9, 18, 23, 28, 35, 32
32회 | 6, 14, 19, 25, 34, 44, 11
33회 | 3, 15, 23, 26, 30, 38, 36
34회 | 9, 26, 35, 37, 40, 42, 2
35회 | 2, 3, 11, 26, 37, 43, 39
36회 | 12, 16, 25, 26, 35, 40, 11
37회 | 7, 27, 30, 33, 35, 37, 42
38회 | 16, 17, 22, 30, 37, 43, 36
39회 | 1, 6, 24, 30, 31, 40, 39
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
