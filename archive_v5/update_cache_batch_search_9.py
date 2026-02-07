import json
import os
import pandas as pd

# Data extracted from search results for rounds 830-846
search_data_raw = """
830회 | 5, 6, 16, 18, 37, 38
831회 | 3, 10, 16, 19, 31, 39
832회 | 13, 14, 19, 26, 40, 43
833회 | 12, 18, 30, 39, 41, 42
834회 | 2, 5, 17, 24, 30, 39
835회 | 1, 17, 26, 27, 31, 38
836회 | 6, 15, 23, 27, 35, 39
837회 | 2, 25, 28, 30, 33, 45
838회 | 9, 14, 17, 33, 36, 38
839회 | 3, 9, 11, 12, 13, 19
840회 | 14, 16, 20, 26, 31, 43
841회 | 6, 14, 17, 20, 24, 39
842회 | 14, 26, 32, 36, 39, 42
843회 | 1, 9, 11, 23, 31, 39
844회 | 7, 8, 13, 15, 33, 45
845회 | 2, 13, 18, 26, 36, 40
846회 | 5, 18, 30, 41, 43, 45
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
