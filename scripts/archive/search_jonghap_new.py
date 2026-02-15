import requests

def search_pano_by_coord(lat, lng):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    # Using Kakao link search with coordinates
    url = f"https://map.kakao.com/link/roadview/{lat},{lng}"
    try:
        response = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
        print(f"Roadview URL for {lat},{lng}: {response.url}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # From Rounds 1133, 1071
    search_pano_by_coord(37.579697, 127.044971)
