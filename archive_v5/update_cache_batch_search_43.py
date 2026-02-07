import json
import os
import pandas as pd

# VERIFIED data for rounds 120-139
verified_data_raw = """
120회 | 4, 6, 10, 11, 32, 37, 30
121회 | 12, 28, 30, 34, 38, 43, 9
122회 | 1, 11, 16, 17, 36, 40, 8
123회 | 7, 17, 18, 28, 30, 45, 27
124회 | 4, 16, 23, 25, 29, 42, 1
125회 | 2, 8, 32, 33, 35, 36, 18
126회 | 7, 20, 22, 27, 40, 43, 1
127회 | 3, 5, 10, 29, 32, 43, 35
128회 | 19, 21, 27, 30, 31, 37, 12
129회 | 19, 23, 25, 28, 38, 42, 17
130회 | 7, 19, 24, 27, 42, 45, 31
131회 | 8, 10, 11, 14, 15, 21, 37
132회 | 3, 17, 23, 34, 41, 45, 43
133회 | 1, 10, 16, 20, 33, 40, 26
134회 | 3, 12, 20, 23, 31, 35, 43
135회 | 6, 14, 22, 28, 35, 39, 16
136회 | 5, 12, 20, 25, 32, 38, 11
137회 | 1, 16, 20, 22, 31, 44, 34
138회 | 3, 11, 16, 25, 29, 43, 9
139회 | 1, 14, 21, 23, 32, 43, 18
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
