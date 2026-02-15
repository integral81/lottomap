
import requests

def resolve_kakao_link(url):
    try:
        r = requests.get(url, allow_redirects=True)
        print(f"Final URL: {r.url}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    resolve_kakao_link("https://kko.to/-6KddnhXWj")
