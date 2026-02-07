import requests
import os

def test_excel_download():
    # URL pattern found from search
    url = "https://www.dhlottery.co.kr/gameResult.do?method=allWinExel&nowPage=1&drwNoStart=1&drwNoEnd=1209"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Referer': 'https://www.dhlottery.co.kr/gameResult.do?method=byWin',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    }
    
    try:
        print(f"[*] Attempting to download from {url}...")
        response = requests.get(url, headers=headers, timeout=20)
        
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', '')
            print(f"[SUCCESS] Received response. Content-Type: {content_type}")
            
            # Save the file
            filename = "lotto_history_official_download.xls"
            with open(filename, "wb") as f:
                f.write(response.content)
            
            print(f"[SUCCESS] File saved as {filename}. Size: {len(response.content)} bytes.")
            
            # Quick check if it's actually an HTML error page or an Excel file
            if b"<html" in response.content[:100].lower():
                print("[WARNING] The downloaded file appears to be HTML, not binary Excel.")
            else:
                print("[INFO] The downloaded file appears to be binary or CSV-Excel.")
            return True
        else:
            print(f"[FAIL] HTTP Status: {response.status_code}")
    except Exception as e:
        print(f"[ERROR] {str(e)}")
    return False

if __name__ == "__main__":
    test_excel_download()
