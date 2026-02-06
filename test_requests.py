import requests
from bs4 import BeautifulSoup

def test_fetch(round_num):
    url = f"https://www.dhlottery.co.kr/store.do?method=topStore&drwNo={round_num}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Check for 1st prize table or content
        # Looking for things like "1등 당첨판매점"
        if "1등 당첨판매점" in response.text:
            print("Found 1st prize data!")
            # Print a bit of content to verify
            print(response.text[:500])
        else:
            print("1st prize data not found in this URL.")

if __name__ == "__main__":
    test_fetch(1209)
