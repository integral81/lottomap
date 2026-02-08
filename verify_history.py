import requests
import json
import time
import os

HISTORY_FILE = 'lotto_history.json'

def load_history():
    if not os.path.exists(HISTORY_FILE):
        print(f"Error: {HISTORY_FILE} not found.")
        return {}
    with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
        # Load as ordered dict to preserve order if possible, though we will re-sort
        return json.load(f)

def save_history(data):
    # Sort keys descending numerically (1210, 1209, ...)
    try:
        sorted_data = dict(sorted(data.items(), key=lambda item: int(item[0]), reverse=True))
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            # Using separators to keep file compact like original: (',', ': ')
            # But standard dump is fine. Let's maximize compatibility.
            json.dump(sorted_data, f, ensure_ascii=False)
    except Exception as e:
        print(f"[Critical Error] Failed to save history: {e}")

def verify_and_correct():
    print(f"[*] Loading {HISTORY_FILE}...")
    data = load_history()
    if not data:
        return

    start_round = 1
    end_round = 1000 # Correcting 1~1000 as requested
    
    print(f"[*] Starting verification for rounds {start_round} to {end_round}...")
    print(f"[*] Delay: 1.0 second per request to verify safely.")
    print(f"[*] You can continue other work while this runs.")
    
    updates_count = 0
    consecutive_errors = 0
    
    for r in range(start_round, end_round + 1):
        round_str = str(r)
        url = f'https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={r}'
        
        try:
            # print(f"Checking Round {r}...", end='\r')
            resp = requests.get(url, timeout=10)
            
            if resp.status_code == 200:
                result = resp.json()
                consecutive_errors = 0 # Reset error count
                
                if result.get('returnValue') == 'success':
                    real_nums = [
                        result['drwtNo1'], result['drwtNo2'], result['drwtNo3'],
                        result['drwtNo4'], result['drwtNo5'], result['drwtNo6']
                    ]
                    real_nums.sort()
                    
                    stored_nums = data.get(round_str)
                    
                    # Sort stored nums for comparison if they exist
                    if stored_nums:
                        stored_nums = sorted(stored_nums)
                    
                    if stored_nums != real_nums:
                        print(f"\n[!] FIX FOUND Round {r}")
                        print(f"    - Old: {stored_nums}")
                        print(f"    - New: {real_nums}")
                        
                        data[round_str] = real_nums
                        save_history(data) # Save immediately
                        updates_count += 1
                    else:
                        # Optional: Print progress every 10 rounds to reduce clutter
                        if r % 10 == 0:
                            print(f"[OK] Verified up to Round {r}", end='\r')
                else:
                    print(f"\n[?] Round {r}: No data found (returnValue != success)")
            else:
                print(f"\n[Error] Round {r}: HTTP {resp.status_code}")
                consecutive_errors += 1
                
        except Exception as e:
            print(f"\n[Exception] Round {r}: {e}")
            consecutive_errors += 1
            
        if consecutive_errors >= 10:
            print(f"\n[Stop] Too many consecutive errors. Stopping verification.")
            break
            
        time.sleep(1.0) # 1 second sleep
        
    print(f"\n\n[*] Verification complete. Total updates: {updates_count}")

if __name__ == "__main__":
    verify_and_correct()
