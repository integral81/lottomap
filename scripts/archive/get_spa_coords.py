import requests
import json

# Convert WCONGNAMUL to WGS84 coordinates
url = 'https://dapi.kakao.com/v2/local/geo/transcoord.json'
params = {
    'x': 512793,
    'y': 1156065,
    'input_coord': 'WCONGNAMUL',
    'output_coord': 'WGS84'
}
headers = {
    'Authorization': 'KakaoAK 84b62e85ed3ec32fca558717eda26006'
}

r = requests.get(url, params=params, headers=headers)
data = r.json()

if 'documents' in data and len(data['documents']) > 0:
    lat = data['documents'][0]['y']
    lng = data['documents'][0]['x']
    print(f"Exact coordinates for 스파:")
    print(f"  lat: {lat}")
    print(f"  lng: {lng}")
else:
    print("Failed to get coordinates")
    print(data)
