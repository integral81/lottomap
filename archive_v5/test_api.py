import requests
import json

def test_api():
    url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=480"
    print(f"Fetching {url}...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.dhlottery.co.kr/'
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        print(f"Status Code: {resp.status_code}")
        # print first 200 chars of text to debug if not json
        print(f"Text snippet: {resp.text[:200]}")
        data = resp.json()
        print("Success!")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api()
