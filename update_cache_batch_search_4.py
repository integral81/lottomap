import json
import os
import pandas as pd

# Data extracted from search results for rounds 930-949
search_data_raw = """
949회 | 14, 21, 35, 36, 40, 44
948회 | 1, 10, 20, 21, 23, 31
947회 | 9, 13, 23, 29, 36, 38
946회 | 4, 25, 27, 33, 38, 45
945회 | 2, 9, 17, 23, 30, 43
944회 | 11, 13, 26, 32, 34, 43
943회 | 13, 21, 26, 37, 38, 40
942회 | 10, 14, 25, 30, 34, 40
941회 | 1, 9, 13, 14, 26, 29
940회 | 11, 12, 17, 25, 35, 41
939회 | 1, 16, 22, 29, 36, 39
938회 | 2, 7, 10, 11, 15, 21
937회 | 2, 9, 11, 12, 15, 31
936회 | 10, 13, 23, 30, 31, 43
935회 | 1, 10, 15, 17, 25, 37
934회 | 12, 16, 20, 24, 29, 44
933회 | 1, 6, 12, 14, 16, 40
932회 | 13, 17, 18, 22, 27, 43
931회 | 1, 2, 11, 16, 31, 32
930회 | 8, 21, 25, 38, 39, 44
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
