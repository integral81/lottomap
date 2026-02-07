import json
import os
import pandas as pd

# VERIFIED data for rounds 520-539
verified_data_raw = """
520회 | 4, 22, 27, 28, 38, 40
521회 | 3, 7, 18, 29, 32, 36
522회 | 4, 5, 13, 14, 37, 41
523회 | 1, 4, 37, 38, 40, 45
524회 | 10, 11, 29, 38, 41, 45
525회 | 11, 23, 26, 29, 39, 44
526회 | 7, 14, 17, 20, 35, 39
527회 | 1, 12, 22, 32, 33, 42
528회 | 5, 17, 25, 31, 39, 40
529회 | 18, 20, 24, 27, 31, 42
530회 | 16, 23, 27, 29, 33, 41
531회 | 1, 5, 9, 21, 27, 35
532회 | 16, 17, 23, 24, 29, 44
533회 | 9, 14, 15, 17, 31, 33
534회 | 10, 24, 26, 29, 37, 38
535회 | 11, 12, 14, 15, 18, 39
536회 | 7, 8, 18, 32, 37, 43
537회 | 12, 23, 26, 30, 36, 43
538회 | 6, 10, 18, 31, 32, 34
539회 | 3, 19, 22, 31, 42, 43
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
