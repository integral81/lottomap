
import requests
import json

API_KEY = "84b62e85ed3ec32fca558717eda26006"

def get_coords(query):
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {"Authorization": f"KakaoAK {API_KEY}"}
    try:
        # Try keyword search first for better accuracy with shop names
        r = requests.get(url, headers=headers, params={"query": query}, timeout=5)
        if r.status_code == 200 and r.json()['documents']:
            doc = r.json()['documents'][0]
            return float(doc['y']), float(doc['x']), doc['place_name'], doc['road_address_name']
            
        # Fallback to address search
        url_addr = "https://dapi.kakao.com/v2/local/search/address.json"
        r = requests.get(url_addr, headers=headers, params={"query": query}, timeout=5)
        if r.status_code == 200 and r.json()['documents']:
            doc = r.json()['documents'][0]
            return float(doc['y']), float(doc['x']), query, doc['address_name']
            
    except Exception as e:
        print(f"Error geocoding {query}: {e}")
    return None, None, None, None

def generate_master_list():
    # 1. Already Recovered (Fixed PanoIDs)
    recovered = [
        {"n": "목화휴게소", "a": "경남 사천시 사천대로 912", "id": 1188272977, "pan": 34.24, "tilt": 0.74},
        {"n": "알리바이(나주점)", "a": "전남 나주시 나주로 142", "id": 1191260182, "pan": 17.27, "tilt": -9.34}
    ]
    
    # 2. Missing (Require Coords for Dynamic View)
    missing_targets = [
        {"n": "황금복권방", "q": "부산 부산진구 가야대로 613"}, # Corrected address
        {"n": "로또휴게실", "q": "경기 용인시 기흥구 용구대로 1885"},
        {"n": "복권명당", "q": "대구 수성구 들안로 243"},
        {"n": "가판점(2호선)", "q": "신도림역 2번출구"}, # Keyword search for better exit finding
        {"n": "GS25(청주주성점)", "q": "청주시 주성로 261"},
        {"n": "CU(수성그린점)", "q": "대구 수성구 달구벌대로 686-17"},
        {"n": "복권판매점", "q": "구례군 봉성로 18"},
        {"n": "CU(구미원평점)", "q": "구미시 구미중앙로 45"},
        {"n": "뉴빅마트", "q": "부산 기장군 정관해해로 50"},
        {"n": "대박찬스", "q": "양주시 칠봉산로 167"}
    ]
    
    final_list = []
    
    # Add recovered first
    for r in recovered:
        final_list.append({
            "name": r['n'],
            "addr": r['a'],
            "type": "STATIC", # Has PanoID
            "panoId": r['id'],
            "pov": {"pan": r['pan'], "tilt": r['tilt'], "zoom": 0},
            "lat": 0, "lng": 0 # Placeholder, will use PanoID
        })
        
    print("Geocoding missing shops...")
    for t in missing_targets:
        lat, lng, place_name, addr = get_coords(t['q'])
        if lat:
            print(f"  OK: {t['n']} -> {lat}, {lng} ({place_name})")
            final_list.append({
                "name": t['n'],
                "addr": addr or t['q'],
                "type": "DYNAMIC", # Needs lookup
                "lat": lat,
                "lng": lng
            })
        else:
            print(f"  FAIL: {t['n']}")
            
    # Write to JSON for HTML generation
    with open('verification_targets.json', 'w', encoding='utf-8') as f:
        json.dump(final_list, f, indent=2, ensure_ascii=False)
        
    print(f"Saved {len(final_list)} targets to verification_targets.json")

if __name__ == "__main__":
    generate_master_list()
