import requests
from bs4 import BeautifulSoup

def debug_fetch():
    url = "https://dhlottery.co.kr/gameResult.do?method=byWin&drwNo=480"
    print(f"Fetching {url}...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {resp.status_code}")
        soup = BeautifulSoup(resp.content, 'html.parser')
        
        win_result = soup.find('div', class_='win_result')
        if win_result:
            print("Found div.win_result")
            print(win_result.prettify()[:500]) # First 500 chars
        else:
            print("NOT FOUND div.win_result")
            # Print body start
            print(soup.body.prettify()[:500] if soup.body else "No body")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_fetch()
