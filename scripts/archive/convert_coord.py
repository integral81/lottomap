
import requests

api_key = "84b62e85ed3ec32fca558717eda26006"
x = 447266
y = 1158548

url = f"https://dapi.kakao.com/v2/local/geo/transcoord.json?x={x}&y={y}&input_coord=WCONGNAMUL&output_coord=WGS84"
headers = {"Authorization": f"KakaoAK {api_key}"}

try:
    response = requests.get(url, headers=headers)
    data = response.json()
    if data.get('documents'):
        doc = data['documents'][0]
        print(f"Lat: {doc['y']}, Lng: {doc['x']}")
    else:
        print(f"Error: {data}")
except Exception as e:
    print(f"Error: {e}")
