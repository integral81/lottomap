import requests

# User provided JavaScript key
KAKAO_JS_KEY = "b29ba13a6dceba9dda144cda55359e59"

def test_kakao_geocoding(key, address):
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": f"KakaoAK {key}"}
    params = {"query": address}
    try:
        response = requests.get(url, headers=headers, params=params)
        print(f"Testing with key type: KakaoAK")
        print(f"Address: {address}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    test_kakao_geocoding(KAKAO_JS_KEY, "서울특별시 중구 세종대로 110")
