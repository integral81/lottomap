import requests
import json

def get_kakao_pov(short_url):
    try:
        # 1. Follow redirect to get full URL
        r = requests.get(short_url, allow_redirects=True)
        full_url = r.url
        print(f"Full URL: {full_url}")
        
        # 2. Extract params (very rough parsing, but effective for this task)
        # Expected format: .../roadview/{panoid}/... or params
        # But Kakao Map links are tricky. Let's just print the URL for manual inspection or simple parsing if standard.
        # Actually, standard Kakao Share URL: https://map.kakao.com/?map_type=TYPE_MAP&target=roadview&panoid=...&pan=...&tilt=...&zoom=...&...
        
        return full_url
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    url = "https://kko.to/ZSr2P4edqF"
    get_kakao_pov(url)
