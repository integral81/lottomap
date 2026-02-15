import requests
import json

API_URL = "https://www.dhlottery.co.kr/gameResult.do?method=allWinExel&gubun=byWin&nowPage=1&drwNoStart=1&drwNoEnd=1210"
HEADERS = {
    'Host': 'www.dhlottery.co.kr',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
}

print(f"Testing API with Session: {API_URL}")
try:
    s = requests.Session()
    s.headers.update(HEADERS)
    
    # 1. Visit main page to get cookies
    print("Visiting main page...")
    s.get("https://www.dhlottery.co.kr/common.do?method=main", timeout=10)
    
    # 2. Call API
    print("Calling API...")
    response = s.get(API_URL, timeout=10)
    
    print(f"Status Code: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type')}")
    print(f"First 100 bytes: {response.text[:100]}")
    
    data = response.json()
    print("JSON Decode Success!")
    # print(json.dumps(data, indent=2, ensure_ascii=False)) 
except Exception as e:
    print(f"Error: {e}")
