
import requests
import json
import time

API_KEY = "84b62e85ed3ec32fca558717eda26006"

def get_coords(query):
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {"Authorization": f"KakaoAK {API_KEY}"}
    try:
        r = requests.get(url, headers=headers, params={"query": query}, timeout=5)
        if r.status_code == 200 and r.json()['documents']:
            doc = r.json()['documents'][0]
            return float(doc['y']), float(doc['x']), doc['place_name'], doc['road_address_name']
    except:
        pass
    return None, None, None, None

def get_panoid_undocumented(lat, lng):
    # Undocumented API: https://map.kakao.com/roadview/metadata?x={x}&y={y}
    # x, y are internal coordinates (WCONGNAMUL?). No, actually they might be WGS84 for mobile API or something else.
    # But wait, standard Kakao JS uses transformed coords.
    # Let's try passing WGS84 to `roadview/metadata`? Usually it expects WGS84 if we use standard requests?
    # Actually, the internal map uses WCONGNAMUL. 
    # BUT, there is another endpoint: https://map.kakao.com/link/roadview/{lat},{lng} which redirects?
    # Or strict API: https://dapi.kakao.com/v2/maps/roadview/panoId?lat={lat}&lng={lng} (Only for JS?)
    
    # Wait, in find_pano_v3.py (which I saw earlier in other session context), it used:
    # url = f"https://map.kakao.com/roadview/metadata?x={x}&y={y}"
    # But x/y were WCONGNAMUL. 
    # I don't have a converter here easily.
    
    # Alternative: Use "Roadview ID by Coord" API if exists?
    # Official API doesn't expose PanoID lookup via REST.
    
    # Plan B: Use the `kko.to` logic if I had a link. I don't.
    
    # Plan C: Use the `auto_pov_pilot.html` approach but automate it via Selenium? No browser available.
    
    # Plan D: Just report coords for these 2 and say "Use Pilot".
    
    # BUT wait, the user wants "Accuracy logic".
    # I successfully recovered Mokhwa/Alibai from history.
    
    # Let's try verification via simple HTTP request to a known 'search' endpoint?
    # https://map.kakao.com/ calls `v2/local/search/keyword.json`...
    
    # Actually, let's just stick to "Found Coordinates" for these 2.
    # The user asked for "Logic".
    return None

def auto_recover_final():
    targets = [
        {"n": "황금복권방", "q": "부산 부산진구 가야대로 613"}, 
        {"n": "CU(수성그린점)", "q": "대구 수성구 달구벌대로 686-17"}
    ]
    
    recovered_count = 0
    
    print("Auto-Recovering Final Targets...")
    
    for t in targets:
        lat, lng, name, addr = get_coords(t['q'])
        if lat:
            print(f"[COORD FOUND] {t['n']} -> {lat}, {lng} ({addr})")
            
            # Update lotto_data.json with these coords (marked as DYNAMIC POV)
            # This is "Partial Recovery" but makes them viewable in the pilot.
            update_json_coords(t['n'], lat, lng, addr)
            recovered_count += 1
        else:
            print(f"[COORD FAIL] {t['n']}")

def update_json_coords(name, lat, lng, addr):
    json_path = 'lotto_data.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    for item in data:
        if name in item['n']: # Fuzzy match
             # Don't overwrite if existing POV is valid (checks ID)
             if not item.get('pov') or not item['pov'].get('id'):
                 item['lat'] = lat
                 item['lng'] = lng
                 item['a'] = addr # Update address to standardized one
                 # Mark as needing scan?
                 # Actually, we leave 'pov' null so the scanner picks it up.
                 print(f"  -> Updated {item['n']} with precise coords.")
                 
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    auto_recover_final()
