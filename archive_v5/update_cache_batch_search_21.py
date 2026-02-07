import json
import os
import pandas as pd

# VERIFIED data for rounds 580-599
verified_data_raw = """
580회 | 5, 7, 9, 11, 32, 35
581회 | 3, 5, 14, 20, 42, 44
582회 | 2, 12, 14, 33, 40, 41
583회 | 8, 17, 27, 33, 40, 44
584회 | 7, 18, 30, 39, 40, 41
585회 | 6, 7, 10, 16, 38, 41
586회 | 2, 7, 12, 15, 21, 34
587회 | 14, 21, 29, 31, 32, 37
588회 | 2, 8, 15, 22, 25, 41
589회 | 6, 8, 28, 33, 38, 39
590회 | 20, 30, 36, 38, 41, 45
591회 | 8, 13, 14, 30, 38, 39
592회 | 2, 5, 6, 13, 28, 44
593회 | 9, 10, 13, 24, 33, 38
594회 | 2, 8, 13, 25, 28, 37
595회 | 8, 24, 28, 35, 38, 40
596회 | 3, 4, 12, 14, 25, 43
597회 | 8, 10, 23, 24, 35, 43
598회 | 4, 12, 24, 33, 38, 45
599회 | 5, 12, 17, 29, 34, 35
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
