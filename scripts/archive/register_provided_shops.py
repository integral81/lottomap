import json

def register_shops():
    json_path = 'lotto_data.json'
    shops_to_register = [
        {
            "search": "부자랑",
            "name": "부자랑",
            "addr": "서울 성동구 둘레15길 8 (성수동1가)",
            "lat": 37.5457, # Approximate/Existing
            "lng": 127.0427, # Approximate/Existing
            "pov": {"id": "1198725466", "pan": 247.57, "tilt": 5.2, "zoom": -3}
        },
        {
            "search": "북부슈퍼",
            "name": "북부슈퍼",
            "addr": "경기 의정부시 가능로125번길 22 (가능동)",
            "lat": 37.7483, # Approximate/Existing
            "lng": 127.0423, # Approximate/Existing
            "pov": {"id": "1174088094", "pan": 46.9, "tilt": 10.25, "zoom": -3}
        }
    ]
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        for shop in shops_to_register:
            count = 0
            for item in data:
                if shop["search"] in item.get('n', ''):
                    item['n'] = shop["name"]
                    item['a'] = shop["addr"]
                    # If Lat/Lng exists and is not 0, keep it unless we have better ones.
                    # For safety, let's keep existing Lat/Lng if they look valid (>0)
                    if not item.get('lat') or item.get('lat') == 0:
                        item['lat'] = shop["lat"]
                    if not item.get('lng') or item.get('lng') == 0:
                        item['lng'] = shop["lng"]
                    
                    item['pov'] = shop["pov"]
                    count += 1
            print(f"Updated {count} records for {shop['name']}.")
            
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    register_shops()
