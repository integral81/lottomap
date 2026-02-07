import json
import os
import pandas as pd

search_data_raw = """
960회 | 2, 18, 24, 30, 32, 45 | 14
961회 | 11, 20, 29, 31, 33, 42 | 43
962회 | 1, 18, 28, 31, 34, 43 | 40
963회 | 6, 12, 19, 23, 34, 42 | 35
964회 | 6, 21, 36, 38, 39, 43 | 30
965회 | 2, 13, 25, 28, 29, 36 | 34
966회 | 1, 21, 25, 29, 34, 37 | 36
967회 | 1, 6, 13, 37, 38, 40 | 9
968회 | 2, 5, 12, 14, 24, 39 | 33
969회 | 3, 9, 10, 29, 40, 45 | 7
970회 | 9, 11, 16, 21, 28, 36 | 5
971회 | 2, 6, 17, 18, 21, 26 | 7
972회 | 3, 6, 17, 23, 37, 39 | 26
973회 | 22, 26, 31, 37, 41, 42 | 24
974회 | 1, 2, 11, 16, 39, 44 | 32
975회 | 7, 8, 9, 17, 22, 24 | 5
976회 | 4, 12, 14, 25, 35, 37 | 2
977회 | 2, 9, 10, 14, 22, 44 | 16
978회 | 1, 7, 15, 32, 34, 42 | 8
979회 | 7, 11, 16, 21, 27, 33 | 24
"""

CACHE_FILE = "lotto_fetch_cache.json"
TEMP_CSV = "lotto_history_backups.csv"

def update_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            cache = json.load(f)
    else:
        cache = {}

    lines = search_data_raw.strip().split("\n")
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
    
    print(f"Updated cache with {len(lines)} rounds. Total in cache: {len(cache)}")

if __name__ == "__main__":
    update_cache()
