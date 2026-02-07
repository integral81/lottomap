import json
import os
import pandas as pd

# Verified data after cross-checking conflicting search results
# Range: 800-829
verified_data_raw = """
800회 | 1, 4, 10, 12, 28, 45
801회 | 17, 25, 28, 37, 43, 44
802회 | 10, 11, 12, 18, 24, 42
803회 | 5, 9, 14, 26, 30, 43
804회 | 1, 10, 13, 26, 32, 36
805회 | 3, 12, 13, 18, 31, 32
806회 | 14, 20, 23, 31, 37, 38
807회 | 6, 10, 18, 25, 34, 35
808회 | 15, 21, 31, 32, 41, 43
809회 | 6, 11, 15, 17, 23, 40
810회 | 5, 10, 13, 21, 39, 43
811회 | 8, 11, 19, 21, 36, 45
812회 | 1, 3, 12, 14, 16, 43
813회 | 11, 30, 34, 35, 42, 44
814회 | 2, 21, 28, 38, 42, 45
815회 | 17, 21, 25, 26, 27, 36
816회 | 12, 18, 19, 29, 31, 39
817회 | 3, 9, 12, 13, 25, 43
818회 | 14, 15, 25, 28, 29, 30
819회 | 16, 25, 33, 38, 40, 45
820회 | 10, 21, 22, 30, 35, 42
821회 | 1, 12, 13, 24, 29, 44
822회 | 9, 18, 20, 24, 27, 36
823회 | 12, 18, 24, 26, 39, 40
824회 | 7, 9, 24, 29, 34, 38
825회 | 8, 15, 21, 31, 33, 38
826회 | 13, 16, 24, 25, 33, 36
827회 | 5, 11, 12, 29, 33, 44
828회 | 4, 7, 13, 29, 31, 39
829회 | 4, 5, 31, 35, 43, 45
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
