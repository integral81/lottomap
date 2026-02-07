import json
import os
import pandas as pd

# Data extracted from search results for rounds 890-909
search_data_raw = """
890회 | 1, 4, 14, 18, 29, 37
891회 | 9, 13, 28, 31, 39, 41
892회 | 4, 9, 17, 18, 26, 42
893회 | 1, 15, 17, 23, 25, 41
894회 | 19, 32, 37, 40, 41, 43
895회 | 16, 26, 31, 38, 39, 41
896회 | 5, 12, 25, 26, 38, 45
897회 | 6, 7, 12, 22, 26, 36
898회 | 18, 21, 28, 35, 37, 42
899회 | 8, 19, 20, 21, 33, 39
900회 | 7, 13, 16, 18, 35, 38
901회 | 5, 18, 20, 23, 30, 34
902회 | 7, 19, 23, 24, 36, 39
903회 | 2, 15, 16, 21, 22, 28
904회 | 2, 6, 8, 26, 43, 45
905회 | 3, 4, 16, 27, 38, 40
906회 | 2, 5, 14, 28, 31, 32
907회 | 21, 27, 29, 38, 40, 44
908회 | 3, 16, 21, 22, 23, 44
909회 | 7, 24, 29, 30, 34, 35
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
