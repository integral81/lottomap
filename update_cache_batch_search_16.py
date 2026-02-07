import json
import os
import pandas as pd

# VERIFIED data for rounds 680-699
verified_data_raw = """
680회 | 4, 10, 19, 29, 32, 42
681회 | 21, 24, 27, 29, 43, 44
682회 | 17, 23, 27, 35, 38, 43
683회 | 6, 13, 20, 27, 28, 40
684회 | 1, 11, 15, 17, 25, 39
685회 | 6, 7, 12, 28, 38, 40
686회 | 7, 12, 15, 24, 25, 43
687회 | 1, 8, 10, 13, 28, 42
688회 | 5, 15, 22, 23, 34, 35
689회 | 7, 17, 19, 30, 36, 38
690회 | 24, 25, 33, 34, 38, 39
691회 | 15, 27, 33, 35, 43, 45
692회 | 3, 11, 14, 15, 32, 36
693회 | 1, 6, 11, 28, 34, 42
694회 | 7, 15, 20, 25, 33, 43
695회 | 4, 18, 26, 33, 34, 38
696회 | 1, 7, 16, 18, 34, 38
697회 | 2, 5, 8, 11, 33, 39
698회 | 3, 11, 13, 21, 33, 37
699회 | 1, 4, 8, 20, 35, 41
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
