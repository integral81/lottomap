import json
import os
import pandas as pd

# VERIFIED data for rounds 760-779
verified_data_raw = """
760회 | 10, 22, 27, 31, 42, 43
761회 | 4, 7, 11, 24, 42, 45
762회 | 1, 3, 12, 21, 26, 41
763회 | 3, 8, 16, 32, 34, 43
764회 | 7, 22, 24, 31, 34, 36
765회 | 1, 3, 8, 12, 42, 43
766회 | 9, 30, 34, 35, 39, 41
767회 | 5, 15, 20, 31, 34, 42
768회 | 7, 27, 29, 30, 38, 44
769회 | 5, 7, 11, 16, 41, 45
770회 | 1, 9, 12, 23, 39, 43
771회 | 6, 10, 17, 18, 21, 29
772회 | 5, 6, 11, 14, 21, 41
773회 | 8, 12, 19, 21, 31, 35
774회 | 12, 15, 18, 28, 34, 42
775회 | 11, 12, 29, 33, 38, 42
776회 | 8, 9, 18, 21, 28, 40
777회 | 6, 12, 17, 21, 34, 37
778회 | 6, 21, 35, 36, 37, 41
779회 | 6, 12, 19, 24, 34, 41
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
