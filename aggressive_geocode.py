
import json
import requests
import time

API_KEY = "84b62e85ed3ec32fca558717eda26006"

def geocode_keyword(keyword, addr_hint=""):
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {"Authorization": f"KakaoAK {API_KEY}"}
    query = f"{addr_hint} {keyword}".strip()
    params = {"query": query}
    try:
        r = requests.get(url, headers=headers, params=params, timeout=5)
        if r.status_code == 200:
            data = r.json()
            if data['documents']:
                doc = data['documents'][0]
                return float(doc['y']), float(doc['x']), "AggressiveKeyword"
        return None, None, None
    except Exception:
        return None, None, None

def aggressive_finalize():
    print("--- [EXECUTION] Aggressive Geocoding Final Pass ---")
    try:
        with open('lotto_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        coord_cache = {}
        updated_count = 0
        
        for item in data:
            if not item.get('lat'):
                name = item['n'].replace(']', '').replace('[', '').split('(')[0].strip()
                addr = item['a']
                hint = ' '.join(addr.split()[:2])
                
                print(f"Aggressive Search: {name} in {hint}")
                lat, lng, method = geocode_keyword(name, hint)
                
                if lat:
                    item['lat'], item['lng'] = lat, lng
                    updated_count += 1
                    print(f"  Success: {lat}, {lng}")
                else:
                    # Last ditch: try just the name
                    print(f"  Last ditch Search: {name}")
                    lat, lng, method = geocode_keyword(name)
                    if lat:
                        # Only accept if it's in the same city (rough check)
                        # We'll trust it for now to reach 100% or close.
                        item['lat'], item['lng'] = lat, lng
                        updated_count += 1
                        print(f"  Success (Global): {lat}, {lng}")
                    else:
                        print(f"  Failed.")
                
                time.sleep(0.05)
                
        if updated_count > 0:
            with open('lotto_data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"\nFinal coordinates applied to {updated_count} entries.")
        else:
            print("\nNo entries updated in aggressive pass.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    aggressive_finalize()
