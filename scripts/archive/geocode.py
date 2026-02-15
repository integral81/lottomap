
import requests

api_key = "84b62e85ed3ec32fca558717eda26006"
address = "전북 정읍시 관통로 102"

url = f"https://dapi.kakao.com/v2/local/search/address.json?query={address}"
headers = {"Authorization": f"KakaoAK {api_key}"}

try:
    response = requests.get(url, headers=headers)
    data = response.json()
    if data.get('documents'):
        doc = data['documents'][0]
        print(f"Lat: {doc['y']}, Lng: {doc['x']}")
    else:
        print("No results found.")
except Exception as e:
    print(f"Error: {e}")
