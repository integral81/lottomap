
import json
import requests
import time

API_KEY = "84b62e85ed3ec32fca558717eda26006"

def geocode(address):
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": f"KakaoAK {API_KEY}"}
    params = {"query": address}
    try:
        r = requests.get(url, headers=headers, params=params, timeout=5)
        if r.status_code == 200:
            data = r.json()
            if data['documents']:
                doc = data['documents'][0]
                return float(doc['y']), float(doc['x'])
        return None, None
    except Exception as e:
        print(f"Error geocoding {address}: {e}")
        return None, None

def fix_null_coords():
    file_path = 'top_shops_4wins.json'
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    fixed_count = 0
    for shop in data:
        if shop.get('lat') is None or shop.get('lng') is None:
            print(f"Geocoding: {shop['n']} ({shop['a']})")
            # Try full address
            lat, lng = geocode(shop['a'])
            
            # If failed, try stripping detail address (after building number or spaces)
            if lat is None:
                # Simple heuristic: take first 3-4 words
                short_addr = ' '.join(shop['a'].split()[:4])
                print(f"  Retrying with shorter address: {short_addr}")
                lat, lng = geocode(short_addr)

            if lat:
                shop['lat'] = lat
                shop['lng'] = lng
                fixed_count += 1
                print(f"  Success: {lat}, {lng}")
            else:
                print(f"  Failed to geocode.")
            
            time.sleep(0.1) # Rate limiting

    if fixed_count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\nFixed {fixed_count} shops. Updating admin_roadview.html...")
        
        # Now update the admin tool template
        try:
            from patch_admin_tool import update_admin_tool
            update_admin_tool()
        except Exception as e:
            print(f"Error updating admin tool: {e}")
    else:
        print("\nNo shops were updated.")

if __name__ == "__main__":
    fix_null_coords()
