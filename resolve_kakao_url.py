import requests

url = "https://kko.to/szQwevz9fZ"
try:
    resp = requests.head(url, allow_redirects=True)
    print(f"Final URL: {resp.url}")
except Exception as e:
    print(f"Error: {e}")
