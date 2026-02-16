
import requests

def test_single():
    # Use coordinates known to have roadview (Busan Golden Lottery)
    # x=129.035398550186, y=35.1583856247962
    url = 'https://map.kakao.com/roadview/metadata?x=129.035398550186&y=35.1583856247962'
    headers = {
        'Referer': 'https://map.kakao.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        r = requests.get(url, headers=headers, timeout=5)
        print(f"Status: {r.status_code}")
        print(f"Headers: {r.headers}")
        print("--- Body Start ---")
        print(r.text[:500])
        print("--- Body End ---")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_single()
