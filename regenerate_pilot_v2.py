
import json
import requests
import re

API_KEY = "84b62e85ed3ec32fca558717eda26006"

def get_coords(address):
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": f"KakaoAK {API_KEY}"}
    try:
        r = requests.get(url, headers=headers, params={"query": address}, timeout=5)
        if r.status_code == 200 and r.json()['documents']:
            doc = r.json()['documents'][0]
            return float(doc['y']), float(doc['x'])
    except Exception as e:
        print(f"Error: {e}")
    return None, None

def regenerate():
    # MANUALLY VERIFIED ADDRESSES
    targets = [
        {"n": "황금복권방", "a": "부산 부산진구 가야대로 613"}, # Corrected from 264-6
        {"n": "복권명당", "a": "대구 수성구 들안로 243"}, # Corrected from 355-12
        {"n": "가판점(2호선)", "a": "서울 구로구 새말로 117-24"}, # Shindorim Exit 2
        {"n": "GS25(청주주성점)", "a": "충북 청주시 청원구 주성로 261"},
        {"n": "목화휴게소", "a": "경남 사천시 사천대로 912"}, # Corrected from 1794
        {"n": "cu(수성그린점)", "a": "대구 수성구 달구벌대로 686-17"},
        {"n": "복권판매점", "a": "전남 구례군 구례읍 봉성로 18"},
        {"n": "CU(구미원평점)", "a": "경북 구미시 구미중앙로 45"},
        {"n": "뉴빅마트", "a": "부산 기장군 정관읍 정관해해로 50"}, # Typo fix
        {"n": "대박찬스", "a": "경기 양주시 칠봉산로 167"}
    ]
    
    valid_list = []
    
    print("--- Regenerating Pilot with Verified Data ---")
    
    for t in targets:
        print(f"Geocoding {t['n']} ({t['a']})...")
        lat, lng = get_coords(t['a'])
        if lat:
            t['lat'] = lat
            t['lng'] = lng
            t['status'] = "VERIFIED_READY"
            valid_list.append(t)
            print(f"  -> OK: {lat}, {lng}")
        else:
            print(f"  -> FAIL")
            
    # Save JSON
    with open('auto_pilot_candidates.json', 'w', encoding='utf-8') as f:
        json.dump(valid_list, f, indent=2, ensure_ascii=False)
        
    # Update HTML
    with open('auto_pov_pilot.html', 'r', encoding='utf-8') as f:
        html = f.read()
        
    new_json = json.dumps(valid_list, ensure_ascii=False, indent=4)
    pattern = r'const targets = \[.*?\];'
    # Use function-based replacement to avoid backslash escaping issues
    new_html = re.sub(pattern, lambda m: f'const targets = {new_json};', html, flags=re.DOTALL)
    
    with open('auto_pov_pilot.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
        
    print(f"\nUpdated auto_pov_pilot.html with {len(valid_list)} verified targets.")

if __name__ == "__main__":
    regenerate()
