import json

def register_batch_18():
    json_path = 'lotto_data.json'
    
    # Shop Data for Batch 18
    batch_data = [
        {
            "search_name": "신나는복권방",
            "name": "신나는복권방",
            "addr": "경기 파주시 문향로 51-1",
            "lat": 37.856521,
            "lng": 126.785172,
            "pov": {"id": "1203061211", "pan": 261.14, "tilt": 7.74, "zoom": -3}
        },
        {
            "search_name": "신명",
            "name": "신명",
            "addr": "서울 강서구 방화2동 620-160",
            "lat": 37.562402,
            "lng": 126.808624,
            "pov": {"id": "1198196294", "pan": 0.39, "tilt": 2.37, "zoom": 0}
        },
        {
            "search_name": "신신마트편의점",
            "name": "신신마트편의점",
            "addr": "전남 목포시 철로마을길 36 (옥암동)",
            "lat": 34.804542,
            "lng": 126.384978,
            "pov": {"id": "1192220319", "pan": 101.24, "tilt": 5.65, "zoom": 0}
        },
        {
            "search_name": "신천하명당",
            "name": "신천하명당",
            "addr": "충남 예산군 예산읍 발연로 1 (이마트24)",
            "lat": 36.698833,
            "lng": 126.829418,
            "pov": {"id": "1178836695", "pan": 100.22, "tilt": 4.79, "zoom": 0}
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
                if shop["search_name"] in name:
                    # Filter by partial address match to avoid false positives for common names
                    region = shop["addr"].split()[0] # 경기, 서울, 전남, 충남
                    if region in addr or region[:2] in addr:
                        match = True
                
                if match:
                    item['n'] = shop["name"]
                    item['a'] = shop["addr"]
                    item['lat'] = shop["lat"]
                    item['lng'] = shop["lng"]
                    item['pov'] = shop["pov"]
                    # If 'closed' key exists, remove it as we are confirming it's active with new POV
                    if 'closed' in item:
                        del item['closed']
                    count += 1
            print(f"Updated {count} records for {shop['name']}.")
            
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    register_batch_18()
