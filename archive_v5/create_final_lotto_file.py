import json
import os
import pandas as pd

# VERIFIED data for rounds 1-19
verified_data_raw = """
1회 | 10, 23, 29, 33, 37, 40, 16
2회 | 9, 13, 21, 25, 32, 42, 2
3회 | 11, 16, 19, 21, 27, 31, 30
4회 | 7, 10, 15, 23, 27, 43, 12
5회 | 18, 20, 27, 36, 39, 43, 3
6회 | 1, 4, 17, 23, 30, 31, 34
7회 | 2, 9, 16, 26, 32, 42, 4
8회 | 2, 6, 17, 28, 30, 39, 33
9회 | 2, 7, 16, 21, 29, 36, 30
10회 | 9, 25, 30, 33, 41, 44, 6
11회 | 1, 7, 9, 11, 20, 42, 45
12회 | 2, 8, 23, 27, 38, 40, 3
13회 | 22, 23, 25, 37, 38, 42, 26
14회 | 3, 4, 9, 20, 22, 40, 31
15회 | 5, 6, 13, 24, 30, 37, 12
16회 | 4, 15, 23, 30, 35, 41, 43
17회 | 3, 4, 9, 17, 32, 37, 1
18회 | 3, 12, 13, 19, 32, 35, 29
19회 | 6, 30, 38, 39, 40, 43, 26
"""

CACHE_FILE = "lotto_fetch_cache.json"
FINAL_XLSX = "lotto_historic_numbers_1_1209_Final.xlsx"

def create_final_file():
    # 1. Update cache with 1-19
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
    
    # 2. Create Final Excel
    # Convert cache to DataFrame
    data_list = list(cache.values())
    df = pd.DataFrame(data_list)
    
    # Ensure all rounds 1-1209 are present
    all_rounds = set(range(1, 1210))
    present_rounds = set(df['회차'].unique())
    missing = all_rounds - present_rounds
    
    if missing:
        print(f"WARNING: Missing rounds in final cache: {missing}")
    else:
        print("All rounds 1-1209 are present.")

    # Sort by round number descending (1209 -> 1)
    df = df.sort_values(by='회차', ascending=False)
    
    # Select columns (only 6 numbers as requested)
    columns = ['회차', '번호1', '번호2', '번호3', '번호4', '번호5', '번호6']
    df = df[columns]
    
    # Save to Excel
    df.to_excel(FINAL_XLSX, index=False)
    print(f" Successfully saved {len(df)} rounds to {FINAL_XLSX}")

if __name__ == "__main__":
    create_final_file()
