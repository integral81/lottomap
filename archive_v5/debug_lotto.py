import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def check_main_page():
    url = "https://www.dhlottery.co.kr/common.do?method=main"
    print(f"Checking {url}...")
    try:
        res = requests.get(url, headers=headers, timeout=10)
        print(f"Status Code: {res.status_code}")
        soup = BeautifulSoup(res.text, 'html.parser')

        element = soup.find('strong', id='lottoDrwNo')
        if element:
            print(f"[OK] Found lottoDrwNo: {element.get_text()}")
        else:
            print("[FAIL] Could not find element with id='lottoDrwNo'")
            with open("debug_main.html", "w", encoding="utf-8") as f:
                f.write(res.text)
            print("Saved debug_main.html")
    except Exception as e:
        print(f"[ERROR] {e}")

def check_round_1210():
    url = "https://www.dhlottery.co.kr/gameResult.do?method=byWin765&drwNo=1210"
    print(f"Checking {url}...")
    try:
        res = requests.get(url, headers=headers, timeout=10)
        print(f"Status Code: {res.status_code}")
        soup = BeautifulSoup(res.text, 'html.parser')
        table = soup.find('table', {'class': 'tbl_data'})
        if table:
            rows = table.find('tbody').find_all('tr')
            print(f"[OK] Found table with {len(rows)} rows.")

        else:
            print("[FAIL] Could not find table with class='tbl_data'")
            with open("debug_round.html", "w", encoding="utf-8") as f:
                f.write(res.text)
            print("Saved debug_round.html")
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    check_main_page()
    check_round_1210()
