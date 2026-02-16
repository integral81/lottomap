import requests
import json

API_KEY = "84b62e85ed3ec32fca558717eda26006"
HEADERS = {"Authorization": f"KakaoAK {API_KEY}"}

def search_address(query):
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    params = {"query": query}
    resp = requests.get(url, headers=HEADERS, params=params)
    return resp.json()

def search_keyword(query, x, y, radius=50):
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    params = {"query": query, "x": x, "y": y, "radius": radius}
    resp = requests.get(url, headers=HEADERS, params=params)
    return resp.json()

target_addr = "경기 여주시 세종로475번길 2"
print(f"Analyzing Address: {target_addr}")

# 1. Get Coordinates
addr_result = search_address(target_addr)
if not addr_result['documents']:
    print("Address not found via API.")
    # Try backup: '점봉동 348-3'
    addr_result = search_address("경기 여주시 점봉동 348-3")

if addr_result['documents']:
    x = addr_result['documents'][0]['x']
    y = addr_result['documents'][0]['y']
    print(f"Coordinates: x={x}, y={y}")
    
    # 2. Search Categories around this point
    keywords = ["편의점", "슈퍼", "유통", "복권", "로또", "마트"]
    for kw in keywords:
        res = search_keyword(kw, x, y, radius=30) # Very tight radius
        if res['documents']:
            print(f"\n[Found '{kw}' nearby]:")
            for doc in res['documents']:
                print(f"- {doc['place_name']} ({doc['category_name']}) - {doc['road_address_name']}")
else:
    print("Could not get coordinates.")
