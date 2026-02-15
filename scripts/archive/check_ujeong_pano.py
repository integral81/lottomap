import requests

def search_pano_for_umi(addr):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    url = f"https://map.kakao.com/link/search/{addr}"
    try:
        response = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
        print(f"Search results for {addr}: {response.url}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    addr = "부산 동래구 온천장로 33"
    search_pano_for_umi(addr)
