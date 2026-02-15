import json

def register_batch_31():
    json_path = 'lotto_data.json'
    
    # Shop Data for Batch 31
    batch_data = [
        {
            "search_name": "터미널복권방",
            "name": "터미널복권방",
            "addr": "전북 정읍시 연지8길 6 (연지동)",
            "lat": 35.572332,
            "lng": 126.844958,
            "pov": {"id": "1183651169", "pan": 76.24, "tilt": 1.15, "zoom": -3}
        },
        {
            "search_name": "토토복권",
            "name": "토토복권",
            "addr": "대구 서구 달서로12길 9 (비산동)",
            "lat": 35.867480,
            "lng": 128.572060,
            "pov": {"id": "1201339587", "pan": 35.30, "tilt": 11.64, "zoom": -3}
        },
        {
            "search_name": "풍전슈퍼",
            "name": "풍전슈퍼",
            "addr": "경기 부천시 원미구 지봉로 428 (역곡동)",
            "lat": 37.497090,
            "lng": 126.791167,
            "pov": {"id": "1203725677", "pan": 175.36, "tilt": 12.10, "zoom": -3}
        }
    ]
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        for shop in batch_data:
            count = 0
            for item in data:
                name = item.get('n', '')
                addr = item.get('a', '')
                
                # Matching logic
                match = False
                if shop["search_name"][:4] in name:
                    region = shop["addr"].split()[0]
                    if region in addr:
                        # Extra city/district check
                        city_dist = shop["addr"].split()[1]
                        if city_dist in addr:
                            match = True
                
                if match:
                    item['n'] = shop["name"]
                    item['a'] = shop["addr"]
                    item['lat'] = shop["lat"]
                    item['lng'] = shop["lng"]
                    item['pov'] = shop["pov"]
                    if 'closed' in item:
                        del item['closed']
                    count += 1
            print(f"Updated {count} records for {shop['name']}.")
            
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    register_batch_31()
