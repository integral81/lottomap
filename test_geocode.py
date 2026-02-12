
import requests
import json

API_KEY = '84b62e85ed3ec32fca558717eda26006'

def geocode(address):
    url = f"https://dapi.kakao.com/v2/local/search/address.json?query={address}"
    headers = {"Authorization": f"KakaoAK {API_KEY}"}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        data = r.json()
        if data['documents']:
            doc = data['documents'][0]
            return {
                'lat': float(doc['y']),
                'lng': float(doc['x']),
                'address': doc['address_name']
            }
    return None

if __name__ == "__main__":
    res = geocode("전남 장성군 영천로 150-1")
    print(json.dumps(res))
