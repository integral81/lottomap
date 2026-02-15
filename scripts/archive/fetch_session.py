
import requests

def fetch_with_session():
    s = requests.Session()
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://dhlottery.co.kr/main.do'
    })
    
    # Visit main page first to get cookies
    try:
        s.get('https://dhlottery.co.kr/common.do?method=main')
        
        # Now fetch the store page
        url = 'https://dhlottery.co.kr/store.do?method=topStore&pageGubun=L645&drwNo=1210'
        r = s.get(url)
        
        with open('round_1210_session.html', 'w', encoding='utf-8') as f:
            f.write(r.text)
            
        print(f"Fetched {len(r.text)} bytes")
        if "1등 배출점" in r.text or "상호명" in r.text:
            print("Content looks good!")
        else:
            print("Content might be missing target table.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_with_session()
