import json
import os
import pandas as pd

# VERIFIED data for rounds 363-379
verified_data_raw = """
363회 | 11, 12, 14, 21, 32, 38, 6
364회 | 2, 5, 7, 14, 16, 40, 4
365회 | 5, 15, 21, 25, 26, 30, 31
366회 | 5, 12, 19, 26, 27, 44, 38
367회 | 3, 22, 25, 29, 32, 44, 19
368회 | 11, 21, 24, 30, 39, 45, 26
369회 | 17, 20, 35, 36, 41, 43, 21
370회 | 16, 18, 24, 42, 44, 45, 17
371회 | 7, 9, 15, 26, 27, 42, 18
372회 | 8, 11, 14, 16, 18, 21, 13
373회 | 15, 26, 37, 42, 43, 45, 9
374회 | 11, 13, 15, 17, 25, 34, 26
375회 | 4, 8, 19, 25, 27, 45, 7
376회 | 1, 11, 13, 24, 28, 40, 7
377회 | 6, 22, 29, 37, 43, 45, 23
378회 | 5, 22, 29, 31, 34, 39, 43
379회 | 6, 10, 22, 31, 35, 40, 19
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
        # Handle 6 numbers + bonus (7 numbers total) if present in raw string
        # The raw string has 7 numbers.
        # But the cache logic needs to put bonus in '보너스' field if schema supports it, 
        # or just 6 numbers. 
        # Wait, previous scripts only cached 6 numbers.
        # Check cache structure in previous steps?
        # Step 1189 script:
        # cache[drw_no_str] = { '회차': ..., '번호1': ..., ... '번호6': ... }
        # It didn't save bonus number!
        # The user's request conversation a2a86194 says: "confirmed that the previous data for rounds 1205-1209 was incorrect and have requested that only the 6 winning numbers (excluding the bonus number) be included in the final output."
        # AH! I SHOULD NOT INCLUDE BONUS NUMBER IN THE OUTPUT EXCEL.
        # But for the cache, should I save it?
        # The prompt says: "Fetch all lottery data from rounds 1 to 1209."
        # But conversation history says "only the 6 winning numbers (excluding the bonus number) be included in the final output."
        # I will stick to the 6 numbers for the cache consistency with previous scripts.
        # The prompt says "fetching remaining lotto data", implying completeness.
        # I'll stick to 6 numbers to be consistent with my previous scripts which only saved 6.
        # The bonus numbers I verified are good for verification but I won't save them if I haven't been.
        # Wait, did I save them before?
        # Let's check `update_cache_batch_search_29.py` content in Step 1286...
        # It wrote: `nums = [int(n.strip()) for n in parts[1].split(",")]` and verified data had 6 numbers.
        # So I only need 6 numbers.
        # I verified bonus numbers primarily to ensure I wasn't getting "hallucinated" data and that I had the full set to cross-reference if needed, and because search results often present them together.
        # So I will just take the first 6 numbers from my verified list.
        
        nums_all = [int(n.strip()) for n in parts[1].split(",")]
        # Take first 6
        nums = nums_all[:6]
        
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
