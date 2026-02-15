import requests

def search_cu_yeoju_ic_pov():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    # Yeoju-eup Jeombong-ri 437-11 -> Sejong-ro 390 (CU Yeoju IC)
    # Approx coords: 37.2662, 127.6321
    url = f"https://map.kakao.com/link/roadview/37.266213,127.632064"
    try:
        response = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
        print(f"Roadview URL for CU Yeoju IC: {response.url}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    search_cu_yeoju_ic_pov()
