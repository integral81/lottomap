import json

def register_batch_17():
    json_path = 'lotto_data.json'
    
    # Shop Data
    batch_data = [
        {
            "search_name": "스카이편의점",
            "name": "스카이편의점",
            "addr": "경기 안양시 만안구 박달로 527 (박달동)",
            "lat": 37.402749,
            "lng": 126.911276,
            "pov": {"id": "1202461052", "pan": 31.72, "tilt": -4.23, "zoom": -3}
        },
        {
            "search_name": "스포츠베팅샵",
            "name": "스포츠베팅샵",
            "addr": "서울 서초구 양재대로11길 36 (양재동 373)",
            "lat": 37.471332,
            "lng": 127.044366,
            "pov": {"id": "1198055150", "pan": 152.71, "tilt": -3.49, "zoom": -3}
        },
        {
            "search_name": "승일유통",
            "name": "승일유통",
            "addr": "충북 청주시 흥덕구 복대동 200-14",
            "lat": 36.638328,
            "lng": 127.453757,
            "pov": {"id": "1170114670", "pan": 24.86, "tilt": 1.6, "zoom": -3}
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
                
                # Matching
                if shop["search_name"] in name:
                    # Filter by region to be safe
                    region = shop["addr"].split()[0] # 경기, 서울, 충북
                    if region in addr or region[:2] in addr:
                        item['n'] = shop["name"]
                        item['a'] = shop["addr"]
                        item['lat'] = shop["lat"]
                        item['lng'] = shop["lng"]
                        item['pov'] = shop["pov"]
                        count += 1
            print(f"Updated {count} records for {shop['name']}.")
            
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    register_batch_17()
