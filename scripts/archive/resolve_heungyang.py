import requests

def resolve_kakao_url(short_url):
    try:
        response = requests.get(short_url, allow_redirects=True)
        print(f"Final URL: {response.url}")
    except Exception as e:
        print(f"Error resolving URL: {e}")

if __name__ == "__main__":
    resolve_kakao_url("https://kko.to/wuUavtCqeJ")
