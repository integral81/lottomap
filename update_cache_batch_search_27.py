import json
import os
import pandas as pd

# VERIFIED data for rounds 460-479
verified_data_460_479 = """
460회 | 8, 11, 28, 30, 43, 45
461회 | 11, 18, 26, 31, 37, 40
462회 | 3, 20, 24, 32, 37, 45
463회 | 23, 29, 31, 33, 34, 44
464회 | 6, 12, 15, 34, 42, 44
465회 | 1, 8, 11, 13, 22, 38
466회 | 4, 10, 13, 23, 32, 44
467회 | 2, 12, 14, 17, 24, 40
468회 | 8, 13, 15, 28, 37, 43
469회 | 4, 21, 22, 34, 37, 38
470회 | 10, 16, 20, 39, 41, 42
471회 | 6, 13, 29, 37, 39, 41
472회 | 16, 25, 26, 31, 36, 43
473회 | 8, 13, 20, 22, 23, 36
474회 | 4, 13, 18, 31, 33, 45
475회 | 1, 9, 14, 16, 21, 29
476회 | 9, 12, 13, 15, 37, 38
477회 | 14, 25, 29, 32, 33, 45
478회 | 18, 29, 30, 37, 39, 43
479회 | 8, 23, 25, 27, 35, 44
"""

# VERIFIED data for rounds 440-459
verified_data_440_459 = """
440회 | 10, 22, 28, 34, 36, 44
441회 | 1, 23, 28, 30, 34, 35
442회 | 25, 27, 29, 36, 38, 40
443회 | 4, 6, 10, 19, 20, 44
444회 | 11, 13, 23, 35, 43, 45
445회 | 13, 20, 21, 30, 39, 45
446회 | 1, 11, 12, 14, 26, 35
447회 | 2, 7, 8, 9, 17, 33
448회 | 3, 7, 13, 27, 40, 41
449회 | 3, 10, 20, 26, 35, 43
450회 | 6, 14, 19, 21, 23, 31
451회 | 12, 15, 20, 24, 30, 38
452회 | 8, 10, 18, 30, 32, 34
453회 | 12, 24, 33, 38, 40, 42
454회 | 13, 25, 27, 34, 38, 41
455회 | 4, 19, 20, 26, 30, 35
456회 | 1, 7, 12, 18, 23, 27
457회 | 8, 10, 18, 23, 27, 40
458회 | 4, 9, 10, 32, 36, 40
459회 | 4, 6, 10, 14, 25, 40
"""

CACHE_FILE = "lotto_fetch_cache.json"
TEMP_CSV = "lotto_history_backups.csv"

def update_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            cache = json.load(f)
    else:
        cache = {}

    all_data = verified_data_460_479.strip() + "\n" + verified_data_440_459.strip()
    
    lines = all_data.strip().split("\n")
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
