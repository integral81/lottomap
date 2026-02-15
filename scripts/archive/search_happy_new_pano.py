import requests

def search_happy_super_new():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    # New address: 서울 성북구 동소문로 49 (동소문동4가 115)
    url = f"https://map.kakao.com/link/roadview/35.568409,128.165411" # Mistake in coord, let me fix
    # Actually, coord for Dongsomun-ro 49 is 37.591021, 127.011144 based on lotto_data.json
    url = f"https://map.kakao.com/link/roadview/37.591021,127.011144"
    try:
        response = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
        print(f"Roadview URL for Happy Super (New): {response.url}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    search_happy_super_new()
