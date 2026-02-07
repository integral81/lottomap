import json
import os
import pandas as pd

# Data extracted from search results for rounds 847-869
search_data_raw = """
847회 | 12, 16, 26, 28, 30, 42
848회 | 1, 2, 16, 22, 38, 39
849회 | 5, 13, 17, 29, 34, 39
850회 | 16, 20, 24, 28, 36, 39
851회 | 14, 18, 22, 26, 31, 44
852회 | 11, 17, 28, 30, 33, 35
853회 | 2, 8, 23, 26, 27, 44
854회 | 20, 25, 31, 32, 36, 43
855회 | 8, 15, 17, 19, 43, 44
856회 | 10, 24, 40, 41, 43, 44
857회 | 6, 10, 16, 28, 34, 38
858회 | 9, 13, 32, 38, 39, 42
859회 | 8, 22, 35, 38, 39, 41
860회 | 4, 8, 18, 25, 27, 32
861회 | 11, 17, 19, 21, 22, 25
862회 | 10, 34, 38, 40, 42, 43
863회 | 3, 7, 10, 13, 25, 36
864회 | 3, 7, 10, 13, 25, 36
865회 | 3, 15, 22, 32, 33, 45
866회 | 9, 15, 29, 34, 37, 39
867회 | 14, 17, 19, 22, 24, 40
868회 | 12, 17, 28, 41, 43, 44
869회 | 2, 6, 20, 27, 37, 39
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
