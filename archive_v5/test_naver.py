import requests
from bs4 import BeautifulSoup

def test_naver():
    # Query: 480회 로또
    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=480%ED%9A%8C+%EB%A1%9C%EB%98%90"
    print(f"Fetching {url}...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {resp.status_code}")
        
        soup = BeautifulSoup(resp.content, 'html.parser')
        
        # Naver Lotto structure often changes.
        # Look for 'win_number' or similar classes.
        # Or look for text "480회 당첨번호"
        
        # Try finding the specific balls (usually have class 'ball')
        # In Naver, they often use classes like 'num_box' or 'winning_number'
        
        # Let's just print all text inside 'div' that contains "당첨번호" to see structure
        # Or just print a snippet of body to analyze
        
        # Targeted search
        # Usually: <div class="num_box"> <span class="ball"> ...
        
        divs = soup.find_all('div', class_='num_box')
        if divs:
            print(f"Found {len(divs)} num_box divs")
            for d in divs:
                print(d.prettify())
        else:
            print("No 'num_box' found. Dumping body snippet:")
            print(soup.body.prettify()[:1000] if soup.body else "No body")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_naver()
