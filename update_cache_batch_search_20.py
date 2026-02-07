import json
import os
import pandas as pd

# VERIFIED data for rounds 600-619
verified_data_raw = """
600회 | 5, 11, 14, 27, 29, 36
601회 | 2, 16, 19, 31, 34, 35
602회 | 13, 14, 22, 27, 30, 38
603회 | 2, 19, 25, 26, 27, 43
604회 | 2, 6, 18, 21, 33, 34
605회 | 1, 2, 7, 9, 10, 38
606회 | 1, 5, 6, 14, 20, 39
607회 | 8, 14, 23, 36, 38, 39
608회 | 4, 8, 18, 19, 39, 44
609회 | 4, 8, 27, 34, 39, 40
610회 | 14, 18, 20, 23, 28, 36
611회 | 2, 22, 27, 33, 36, 37
612회 | 6, 9, 18, 19, 25, 33
613회 | 7, 8, 11, 16, 41, 44
614회 | 8, 21, 25, 39, 40, 44
615회 | 10, 17, 18, 19, 23, 27
616회 | 5, 13, 18, 23, 40, 45
617회 | 4, 5, 11, 12, 24, 27
618회 | 8, 16, 25, 30, 42, 43
619회 | 6, 8, 13, 30, 35, 40
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
