import requests

def search_pano_by_addr(addr):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    # Using Kakao link search with address
    url = f"https://map.kakao.com/link/roadview/{addr}"
    try:
        response = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
        print(f"Roadview URL for {addr}: {response.url}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # The new address is 참외전로 268
    search_pano_by_addr("인천 미추홀구 참외전로 268")
