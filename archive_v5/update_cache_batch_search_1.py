import json
import os
import pandas as pd

# Data extracted from search results for rounds 980-999
search_data_raw = """
980회 | 3, 13, 16, 23, 24, 35 | 14
981회 | 27, 36, 37, 41, 43, 45 | 32
982회 | 5, 7, 13, 20, 21, 44 | 33
983회 | 13, 23, 26, 31, 35, 43 | 15
984회 | 3, 10, 23, 35, 36, 37 | 18
985회 | 17, 21, 23, 30, 34, 44 | 19
986회 | 7, 10, 16, 28, 41, 42 | 40
987회 | 2, 4, 15, 23, 29, 38 | 7
988회 | 2, 13, 20, 30, 31, 41 | 27
989회 | 17, 18, 21, 27, 29, 33 | 26
990회 | 2, 4, 25, 26, 36, 37 | 28
991회 | 13, 18, 25, 31, 33, 44 | 38
992회 | 12, 20, 26, 33, 44, 45 | 24
993회 | 6, 14, 16, 18, 24, 42 | 44
994회 | 1, 3, 8, 24, 27, 35 | 28
995회 | 1, 4, 13, 29, 38, 39 | 7
996회 | 6, 11, 15, 24, 32, 39 | 28
997회 | 4, 7, 14, 16, 24, 44 | 20
998회 | 13, 17, 18, 20, 42, 45 | 41
999회 | 1, 3, 9, 14, 18, 28 | 34
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
        # Bonus skip for now as per previous manual verification rounds, 
        # but let's check if the user wanted it. 
        # User said "6자리 당첨 번호만 포함된 깔끔한 엑셀". 
        # So I'll exclude bonus.
        
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
