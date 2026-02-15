import requests

def resolve_kakao_link(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
        print(f"Final URL: {response.url}")
        
    except Exception as e:
        print(f"Error resolving link: {e}")

if __name__ == "__main__":
    url = "https://kko.to/nKhYfuAaFQ"
    resolve_kakao_link(url)
