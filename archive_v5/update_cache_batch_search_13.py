import json
import os
import pandas as pd

# VERIFIED data for rounds 740-759
verified_data_raw = """
740회 | 4, 8, 9, 16, 17, 19
741회 | 6, 15, 17, 18, 25, 33
742회 | 8, 10, 13, 36, 37, 40
743회 | 15, 19, 21, 34, 41, 44
744회 | 10, 15, 18, 21, 34, 41
745회 | 1, 2, 3, 9, 12, 23
746회 | 1, 10, 11, 24, 25, 40
747회 | 7, 9, 12, 14, 23, 28
748회 | 3, 10, 13, 22, 31, 32
749회 | 12, 14, 24, 26, 34, 45
750회 | 1, 2, 15, 19, 24, 36
751회 | 3, 4, 16, 20, 28, 44
752회 | 4, 16, 20, 33, 40, 43
753회 | 2, 17, 19, 24, 37, 41
754회 | 2, 8, 17, 24, 29, 31
755회 | 13, 14, 26, 28, 30, 36
756회 | 10, 14, 16, 18, 27, 28
757회 | 6, 7, 11, 17, 33, 44
758회 | 5, 9, 12, 30, 39, 43
759회 | 9, 33, 36, 40, 42, 43
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
