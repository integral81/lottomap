import json
import os
import pandas as pd

# Data extracted from search results for rounds 910-929
search_data_raw = """
910회 | 1, 11, 17, 27, 35, 39
911회 | 4, 5, 12, 14, 32, 42
912회 | 5, 8, 18, 21, 22, 38
913회 | 6, 14, 16, 21, 27, 37
914회 | 16, 19, 24, 33, 42, 44
915회 | 2, 6, 11, 13, 22, 37
916회 | 6, 21, 22, 32, 35, 36
917회 | 1, 3, 23, 24, 27, 43
918회 | 7, 11, 12, 31, 33, 38
919회 | 9, 14, 17, 18, 42, 44
920회 | 2, 3, 26, 33, 34, 43
921회 | 5, 7, 12, 22, 28, 41
922회 | 2, 6, 13, 17, 27, 43
923회 | 3, 17, 18, 23, 36, 41
924회 | 3, 11, 34, 42, 43, 44
925회 | 13, 24, 32, 34, 39, 42
926회 | 10, 16, 18, 20, 25, 31
927회 | 4, 15, 22, 38, 41, 43
928회 | 3, 4, 10, 20, 28, 44
929회 | 7, 9, 12, 15, 19, 23
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
