
import json
import requests
import math
import time
import os

# Kakao API Key
API_KEY = "84b62e85ed3ec32fca558717eda26006"

def get_coords(address):
    # Try exact address first
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": f"KakaoAK {API_KEY}"}
    try:
        r = requests.get(url, headers=headers, params={"query": address}, timeout=5)
        if r.status_code == 200 and r.json()['documents']:
            doc = r.json()['documents'][0]
            return float(doc['y']), float(doc['x'])
        else:
            print(f"  [Address Fail] {r.status_code} {r.text[:100]}")
    except Exception as e:
        print(f"  [Address Error] {e}")

    # Fallback: Keyword Search (City + Name)
    # Extract City/Gu from address (first 2 words)
    terms = address.split()
    if len(terms) >= 2:
        short_addr = f"{terms[0]} {terms[1]}"
        # We need the shop name, but the function arg is just address.
        # We'll need to pass name to this function or extract it from context.
        # Let's adjust the function signature in the calling loop instead.
        pass
        
    return None, None

def get_coords_v2(name, address):
    # 1. Try Address
    lat, lng = get_coords(address)
    if lat: return lat, lng
    
    # 2. Try Keyword (Addr prefix + Name)
    terms = address.split()
    if len(terms) >= 2:
        query = f"{terms[0]} {terms[1]} {name}"
        print(f"  [Fallback] Keyword Search: {query}")
        url = "https://dapi.kakao.com/v2/local/search/keyword.json"
        headers = {"Authorization": f"KakaoAK {API_KEY}"}
        try:
            r = requests.get(url, headers=headers, params={"query": query}, timeout=5)
            if r.status_code == 200 and r.json()['documents']:
                doc = r.json()['documents'][0]
                return float(doc['y']), float(doc['x'])
        except Exception as e:
            print(f"  [Keyword Error] {e}")
            
    return None, None

def get_nearest_pano(lat, lng):
    # Kakao Maps API doesn't have a public 'nearestPanoId' endpoint documented for REST, 
    # but we can assume the user might have some internal way or we skip this if not possible via REST.
    # WAIT - The user's `full_recovery.py` used `rvClient.getNearestPanoId` in JS.
    # We cannot do this in Python easily without a valid endpoint.
    # HOWEVER, we can stick to geocoding and creating a "Review List" where the user just clicks "Auto Angle".
    
    # Actually, for this "Heuristic Agent", if we can't find PanoID via REST, 
    # we will generate a "Click to Find" link that opens the map at coords.
    
    # BUT the user asked for "Analysis or OCR". 
    # Since we can't run JS in Python, we will generate a CANDIDATE LIST 
    # that pre-fills the coordinates and calculates the likely ANGLE based on the road direction if we had road data.
    
    # Strategy: 
    # 1. We verify coordinates.
    # 2. We allow the JS frontend to do the `getNearestPanoId`.
    # 3. We create a special "Auto-Recovery Mode" in admin_pov.html that iterates these 10 items 
    #    and AUTOMATICALLY triggers `getNearestPanoId` + `computeAngle` in the browser.
    pass

def generate_pilot_list():
    print("--- Generating Auto-Recovery Pilot List ---")
    
    # Top 10 from previous step
    targets = [
        {"n": "황금복권방", "a": "부산 부산진구 가야대로 264-6 (개금동)"},
        {"n": "복권명당", "a": "대구 수성구 들안로 355-12 (수성동4가)"},
        {"n": "가판점(2호선)", "a": "서울 구로구 남부순환로 1055 (가리봉동)"}, # Adjusted addr
        {"n": "GS25(청주주성점)", "a": "충북 청주시 청원구 주성로 261 (주성동)"},
        {"n": "목화휴게소", "a": "경남 사천시 사천대로 1794 (용현면)"},
        {"n": "cu(수성그린점)", "a": "대구 수성구 달구벌대로 686-17 (사월동)"},
        {"n": "복권판매점", "a": "전남 구례군 구례읍 봉성로 18"},
        {"n": "CU(구미원평점)", "a": "경북 구미시 구미중앙로 45"},
        {"n": "뉴빅마트", "a": "부산 기장군 정관읍 정관해해로 50"}, # Typo fix from user list logic
        {"n": "대박찬스", "a": "경기 양주시 칠봉산로 167"} 
    ]
    
    results = []
    
    for t in targets:
        print(f"Processing {t['n']}...")
        lat, lng = get_coords_v2(t['n'], t['a'])
        
        if lat:
            t['lat'] = lat
            t['lng'] = lng
            t['status'] = "READY_FOR_BROWSER_AUTO"
            results.append(t)
            print(f"  -> Coords: {lat}, {lng}")
        else:
            t['status'] = "GEOCODING_FAILED"
            results.append(t)
            print(f"  -> Failed to geocode")
            
    with open('auto_pilot_candidates.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
        
    print(f"Generated {len(results)} pilot candidates.")

if __name__ == "__main__":
    generate_pilot_list()
