import json

def register_batch_29():
    json_path = 'lotto_data.json'
    
    # Shop Data for Batch 29
    batch_data = [
        {
            "search_name": "천안역로또토토",
            "name": "천안역로또토토복권방",
            "addr": "충남 천안시 동남구 대흥로 219 (대흥동)",
            "lat": 36.809150,
            "lng": 127.147743,
            "pov": {"id": "1195017105", "pan": 185.94, "tilt": 3.33, "zoom": -3}
        },
        {
            "search_name": "천하제일복권명당연무점",
            "name": "천하제일복권명당연무점",
            "addr": "충남 논산시 연무읍 안심현로 79",
            "lat": 36.135468,
            "lng": 127.100078,
            "pov": {"id": "1177151197", "pan": 292.18, "tilt": 6.09, "zoom": -3}
        },
        {
            "search_name": "최강복권&아이스크림",
            "name": "최강복권&아이스크림",
            "addr": "경기 고양시 덕양구 화신로 272번길 38 (화정동)",
            "lat": 37.649694,
            "lng": 126.832722, # Using more precise coordinates for Choigang if needed, but keeping consistent with search
            "pov": {"id": "1203868168", "pan": 169.58, "tilt": 5.89, "zoom": -3}
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
    register_batch_29()
