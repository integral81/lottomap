import requests
import time
import pandas as pd
import os

def download_with_session():
    # Target official Excel export URL
    url = "https://www.dhlottery.co.kr/gameResult.do?method=allWinExel&gubun=byWin&drwNoStart=1&drwNoEnd=1209"
    landing_url = "https://www.dhlottery.co.kr/gameResult.do?method=byWin"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': 'https://www.google.com/'
    }

    session = requests.Session()
    
    print("[*] visiting landing page to establish session...")
    try:
        # First hit the main page to get cookies and bypass initial tracer
        res = session.get(landing_url, headers=headers)
        print(f"[*] Landing page status: {res.status_code}")
        time.sleep(2) # Respect the server/waiting room
        
        # Now try to download the Excel
        headers['Referer'] = landing_url
        print("[*] Requesting full Excel export...")
        res = session.get(url, headers=headers)
        
        if res.status_code == 200:
            if "サービスに接近中です" in res.text or "rsaModulus" in res.text:
                print("[ERR] Still hitting the waiting room/RSA challenge.")
            else:
                with open("lotto_full_raw.xls", "wb") as f:
                    f.write(res.content)
                print(f"[OK] Downloaded {len(res.content)} bytes to lotto_full_raw.xls")
                return True
        else:
            print(f"[ERR] Status code: {res.status_code}")
            
    except Exception as e:
        print(f"[EXC] {str(e)}")
    
    return False

if __name__ == "__main__":
    download_with_session()
