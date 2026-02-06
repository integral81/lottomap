import requests
import pandas as pd
import io

def test_fetch(round_num):
    # This URL is often used for the list of 1st prize winners
    # method=topStore (1st prize shops)
    url = f"https://www.dhlottery.co.kr/store.do?method=topStore&drwNo={round_num}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            # Try to read tables from the HTML
            tables = pd.read_html(io.StringIO(response.text))
            print(f"Found {len(tables)} tables.")
            for i, table in enumerate(tables):
                print(f"\nTable {i}:")
                print(table.head())
                if '상호명' in table.columns or '판매점' in table.columns:
                    print("!!! Detected valid data table !!!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_fetch(1209)
