import json

def register_batch_21():
    json_path = 'lotto_data.json'
    
    # Shop Data for Batch 21
    batch_data = [
        {
            "search_name": "왕대박",
            "name": "왕대박",
            "addr": "부산 동래구 사직3동 140-33",
            "lat": 35.201053,
            "lng": 129.074079,
            "pov": {"id": "1202552695", "pan": 249.86, "tilt": 5.13, "zoom": -3}
        },
        {
            "search_name": "용꿈돼지꿈",
            "name": "용꿈돼지꿈",
            "addr": "인천 부평구 동암남로 11",
            "lat": 37.470993,
            "lng": 126.704830,
            "pov": {"id": "1199049005", "pan": 357.64, "tilt": -3.75, "zoom": -3}
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
                if shop["search_name"] == name: # Exact name match for "왕대박" to avoid confusion with "왕대박복권방" etc.
                    region = shop["addr"].split()[0]
                    if region in addr:
                        # For 왕대박, also check Dongrae
                        if shop["search_name"] == "왕대박" and "동래" not in addr:
                            continue
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
    register_batch_21()
