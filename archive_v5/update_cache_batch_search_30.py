import json
import os
import pandas as pd

# VERIFIED data for rounds 380-399
verified_data_raw = """
380회 | 12, 16, 21, 23, 30, 31
381회 | 11, 14, 21, 28, 30, 44
382회 | 10, 11, 13, 24, 29, 36
383회 | 4, 15, 28, 33, 37, 40
384회 | 13, 15, 17, 33, 36, 40
385회 | 2, 17, 19, 23, 27, 35
386회 | 4, 18, 22, 29, 36, 43
387회 | 3, 4, 10, 16, 36, 43
388회 | 1, 5, 20, 24, 25, 30
389회 | 4, 10, 17, 24, 32, 45
390회 | 6, 12, 23, 32, 38, 41
391회 | 10, 11, 18, 22, 28, 39
392회 | 1, 3, 7, 8, 24, 42
393회 | 10, 17, 20, 25, 34, 42
394회 | 1, 13, 20, 22, 25, 28
395회 | 7, 10, 15, 16, 35, 43
396회 | 1, 2, 16, 25, 30, 39
397회 | 12, 13, 17, 22, 25, 33
398회 | 10, 15, 20, 23, 42, 44
399회 | 1, 2, 9, 17, 19, 42
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
