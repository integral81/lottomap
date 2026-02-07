import requests
import pandas as pd
import time
import os

def fetch_lotto_range(start_round, end_round):
    results = []
    print(f"[*] Fetching rounds {start_round} to {end_round}...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Referer': 'https://www.dhlottery.co.kr/gameResult.do?method=byWin'
    }
    
    for drw_no in range(end_round, start_round - 1, -1):
        url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={drw_no}"
        try:
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code == 200:
                try:
                    data = res.json()
                    if data.get("returnValue") == "success":
                        results.append({
                            '회차': data['drwNo'],
                            '추첨일': data['drwNoDate'],
                            '번호1': data['drwtNo1'],
                            '번호2': data['drwtNo2'],
                            '번호3': data['drwtNo3'],
                            '번호4': data['drwtNo4'],
                            '번호5': data['drwtNo5'],
                            '번호6': data['drwtNo6']
                        })
                        print(f"[OK] Round {drw_no} fetched.")
                    else:
                        print(f"[FAIL] Round {drw_no} not found.")
                except Exception:
                    print(f"[ERR] Non-JSON response for round {drw_no}. Length: {len(res.text)}")
                    if "rsaModulus" in res.text or "서비스 접근 대기" in res.text:
                        print("  -> Waiting room detected.")
            else:
                print(f"[ERR] Status {res.status_code} for round {drw_no}")
            
            time.sleep(1) # Be more patient
        except Exception as e:
            print(f"[EXC] Round {drw_no}: {str(e)}")
            
    return results

if __name__ == "__main__":
    # Fetch 50 rounds first (1160 to 1209)
    end = 1209
    start = 1160
    
    data_list = fetch_lotto_range(start, end)
    
    if data_list:
        df = pd.DataFrame(data_list)
        df = df.sort_values(by='회차', ascending=False)
        output_file = "lotto_historic_numbers_1_1209_Final.xlsx"
        df.to_excel(output_file, index=False)
        print(f"\n[SUCCESS] Saved to {output_file}")
    else:
        print("[FAIL] No data fetched.")
