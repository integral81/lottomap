import json
import os
import pandas as pd

# Data extracted from search results for rounds 870-889
search_data_raw = """
870회 | 21, 25, 30, 32, 40, 42
871회 | 2, 6, 12, 26, 30, 34
872회 | 10, 16, 23, 25, 32, 34
873회 | 3, 5, 12, 13, 33, 39
874회 | 1, 15, 17, 23, 27, 43
875회 | 1, 8, 12, 29, 39, 44
876회 | 5, 16, 21, 26, 34, 42
877회 | 5, 17, 18, 22, 23, 43
878회 | 2, 6, 11, 16, 25, 31
879회 | 10, 12, 17, 36, 38, 41
880회 | 7, 17, 19, 23, 24, 45
881회 | 4, 18, 20, 26, 27, 32
882회 | 18, 34, 39, 43, 44, 45
883회 | 9, 18, 32, 33, 37, 44
884회 | 4, 14, 23, 28, 37, 45
885회 | 1, 3, 24, 27, 39, 45
886회 | 19, 23, 28, 37, 42, 45
887회 | 8, 14, 17, 27, 36, 45
888회 | 1, 19, 21, 28, 36, 44
889회 | 3, 13, 29, 38, 39, 42
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
