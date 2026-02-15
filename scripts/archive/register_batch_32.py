import json

def register_batch_32():
    json_path = 'lotto_data.json'
    
    # Shop Data for Batch 32
    batch_data = [
        {
            "search_name": "하나마트(하남4번로)",
            "name": "하나마트(하남4번로)",
            "addr": "광주 광산구 하남대로 74번길 6 (장덕동 992-12)",
            "lat": 35.190753,
            "lng": 126.809248,
            "pov": {"id": "1200040582", "pan": 83.69, "tilt": -1.10, "zoom": -3}
        },
        {
            "search_name": "하나복권(가로판매점)",
            "name": "하나복권(가로판매점)",
            "addr": "서울 영등포구 여의나루로 42 가로판매점 (여의도동)",
            "lat": 37.521470,
            "lng": 126.924971,
            "pov": {"id": "1198436250", "pan": 81.84, "tilt": 6.86, "zoom": -1}
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
    register_batch_32()
