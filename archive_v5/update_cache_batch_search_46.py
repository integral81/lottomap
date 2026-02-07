import json
import os
import pandas as pd

# VERIFIED data for rounds 60-79
verified_data_raw = """
60회 | 2, 8, 25, 36, 39, 42, 11
61회 | 14, 15, 19, 30, 38, 43, 8
62회 | 3, 8, 15, 27, 29, 35, 21
63회 | 3, 20, 23, 36, 38, 40, 5
64회 | 14, 15, 18, 21, 26, 36, 39
65회 | 4, 25, 33, 36, 40, 43, 39
66회 | 1, 7, 10, 15, 20, 36, 24
67회 | 3, 7, 10, 15, 36, 38, 33
68회 | 10, 12, 15, 16, 26, 39, 38
69회 | 5, 8, 14, 15, 19, 39, 35
70회 | 5, 19, 22, 25, 28, 43, 26
71회 | 5, 9, 12, 16, 29, 41, 21
72회 | 2, 4, 11, 17, 26, 27, 1
73회 | 3, 12, 18, 32, 40, 43, 38
74회 | 6, 15, 17, 18, 35, 40, 23
75회 | 2, 5, 24, 32, 34, 44, 28
76회 | 1, 3, 15, 22, 25, 37, 43
77회 | 2, 18, 29, 32, 43, 44, 37
78회 | 1, 8, 11, 28, 38, 45, 44
79회 | 3, 12, 24, 27, 30, 32, 14
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
