import json
import os
import pandas as pd

# VERIFIED data for rounds 540-559
verified_data_raw = """
540회 | 3, 12, 13, 15, 34, 36
541회 | 8, 13, 26, 28, 32, 34
542회 | 5, 6, 19, 26, 41, 45
543회 | 13, 18, 26, 31, 34, 44
544회 | 5, 17, 21, 25, 36, 44
545회 | 4, 24, 25, 27, 34, 35
546회 | 8, 17, 20, 27, 37, 43
547회 | 6, 7, 15, 22, 34, 39
548회 | 1, 12, 13, 21, 32, 45
549회 | 29, 31, 35, 38, 40, 44
550회 | 1, 7, 14, 20, 34, 37
551회 | 3, 6, 20, 24, 27, 44
552회 | 1, 10, 20, 32, 35, 40
553회 | 2, 7, 17, 28, 29, 39
554회 | 13, 14, 17, 32, 41, 42
555회 | 11, 17, 21, 24, 26, 36
556회 | 12, 20, 23, 28, 30, 44
557회 | 4, 20, 26, 28, 35, 40
558회 | 12, 15, 19, 26, 40, 43
559회 | 11, 12, 25, 32, 44, 45
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
