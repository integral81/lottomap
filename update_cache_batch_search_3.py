import json
import os
import pandas as pd

search_data_raw = """
950회 | 3, 4, 15, 22, 28, 40
951회 | 2, 12, 30, 31, 39, 43
952회 | 4, 12, 22, 24, 33, 41
953회 | 7, 9, 22, 27, 37, 42
954회 | 1, 9, 26, 28, 30, 41
955회 | 4, 9, 23, 26, 29, 33
956회 | 10, 11, 20, 21, 25, 41
957회 | 4, 15, 24, 35, 36, 40
958회 | 2, 9, 10, 16, 35, 37
959회 | 1, 14, 15, 24, 40, 41
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
