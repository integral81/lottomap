import requests

url = "https://kko.to/Z69tnJrBUp"
try:
    resp = requests.get(url, allow_redirects=True)
    print(f"Final URL: {resp.url}")
except Exception as e:
    print(f"Error: {e}")
