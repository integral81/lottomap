import requests

def search_happy_ppl_pano():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    # Gyeongchung-daero 763 (Konjiam-eup)
    # The coordinate for this is roughly 37.3519, 127.3236 based on common map results
    url = f"https://map.kakao.com/link/roadview/37.351930,127.323580"
    try:
        response = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
        print(f"Roadview URL for Happy People (Konjiam): {response.url}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    search_happy_ppl_pano()
