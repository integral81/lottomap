
import requests
import re

url = "https://kko.to/Zmk9N7xqoU"
try:
    resp = requests.get(url, allow_redirects=True)
    final_url = resp.url
    print(f"Final URL: {final_url}")
except Exception as e:
    print(f"Error: {e}")
