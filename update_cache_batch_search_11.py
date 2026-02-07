import json
import os
import pandas as pd

# VERIFIED data for rounds 780-799
# Each round was cross-checked with official citations because bulk summaries were found to be inaccurate.
verified_data_raw = """
780회 | 15, 17, 19, 21, 27, 45
781회 | 11, 16, 18, 19, 24, 39
782회 | 6, 18, 31, 34, 38, 45
783회 | 14, 15, 16, 17, 38, 45
784회 | 3, 11, 15, 23, 29, 39
785회 | 1, 13, 22, 29, 36, 43
786회 | 1, 2, 7, 21, 24, 34
787회 | 5, 6, 13, 16, 27, 28
788회 | 1, 10, 11, 16, 21, 30
789회 | 2, 6, 7, 12, 19, 45
790회 | 3, 8, 19, 27, 30, 41
791회 | 2, 10, 12, 31, 33, 42
792회 | 12, 21, 25, 34, 38, 43
793회 | 1, 10, 24, 33, 35, 41
794회 | 10, 15, 17, 21, 23, 31
795회 | 1, 11, 20, 26, 32, 43
796회 | 2, 12, 19, 21, 27, 44
797회 | 7, 12, 18, 25, 30, 31
798회 | 14, 21, 22, 25, 33, 43
799회 | 12, 17, 23, 34, 42, 45
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
