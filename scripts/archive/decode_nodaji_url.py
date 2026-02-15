
import requests

def decode_url():
    url = "https://kko.to/GfuAFR_jgC"
    try:
        r = requests.get(url, allow_redirects=False)
        redirect_url = r.headers.get('Location')
        print(f"Redirect URL: {redirect_url}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    decode_url()
