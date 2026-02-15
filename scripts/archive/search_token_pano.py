import requests

def search_pano_near_yu_exit5():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    # Yeungnam Univ Station Exit 5 is roughly 35.8373, 128.7538
    url = f"https://map.kakao.com/link/roadview/35.837260,128.753730"
    try:
        response = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
        print(f"Roadview URL for YU Exit 5: {response.url}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    search_pano_near_yu_exit5()
