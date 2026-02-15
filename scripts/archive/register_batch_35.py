import json

def register_batch_35():
    json_path = 'lotto_data.json'
    
    batch_data = [
        {
            "search_name": "현아상회",
            "name": "현아상회",
            "addr": "부산 남구 용호로 30 (용호동 371-13)",
            "lat": 35.119738,
            "lng": 129.112683,
            "pov": {"id": "1202621150", "pan": 9.86, "tilt": 3.93, "zoom": -3},
            "region": "부산"
        },
        {
            "search_name": "호반할인마트",
            "name": "호반할인마트",
            "addr": "광주 광산구 도산로9번길 40 (도산동 1295-8)",
            "lat": 35.127925,
            "lng": 126.790086,
            "pov": {"id": "1200129904", "pan": 291.63, "tilt": 3.77, "zoom": -3},
            "region": "광주"
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
                
                if shop["search_name"][:3] in name and shop["region"] in addr:
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
    register_batch_35()
