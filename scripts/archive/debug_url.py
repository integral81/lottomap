import requests

url = "https://kko.to/dBhXHdiSEF"
try:
    response = requests.get(url, allow_redirects=True, timeout=10)
    print(f"Final URL: {response.url}")
    # Kakao Roadview URLs often look like:
    # https://map.kakao.com/?panoid=...&pan=...&tilt=...&zoom=...
    # or they might be mobile links.
except Exception as e:
    print(f"Error: {e}")
