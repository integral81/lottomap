import json

def register_batch_30():
    json_path = 'lotto_data.json'
    
    # Shop Data for Batch 30
    batch_data = [
        {
            "search_name": "코리아마트(비산점)",
            "name": "코리아마트(비산점)",
            "addr": "대구 서구 국채보상로 368-2 (비산동)",
            "lat": 35.872426,
            "lng": 128.568712,
            "pov": {"id": "1201556335", "pan": 6.76, "tilt": 0.71, "zoom": -3}
        },
        {
            "search_name": "코사마트금강점",
            "name": "코사마트금강점",
            "addr": "대구 달서구 용산로 204 (용산동)",
            "lat": 35.855734,
            "lng": 128.530832,
            "pov": {"id": "1201616618", "pan": 83.46, "tilt": 4.38, "zoom": -3}
        },
        {
            "search_name": "태원정보통신",
            "name": "태원정보통신",
            "addr": "서울 중랑구 망우로 288 (상봉동)",
            "lat": 37.595433,
            "lng": 127.089685,
            "pov": {"id": "1198250377", "pan": 140.16, "tilt": 3.56, "zoom": -3}
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
                        # City check
                        city = shop["addr"].split()[1]
                        if city in addr:
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
    register_batch_30()
