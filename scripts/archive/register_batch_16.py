import json

def register_batch_16():
    json_path = 'lotto_data.json'
    
    # Shop Data
    batch_data = [
        {
            "search_name": "세류보석복권방",
            "name": "세류보석복권방",
            "addr": "경기 수원시 권선구 경수대로 233 (세류동 1090-7)",
            "lat": 37.254873,
            "lng": 127.015883,
            "pov": {"id": "1200002115", "pan": 105.98, "tilt": 2.44, "zoom": -3}
        },
        {
            "search_name": "세방매점",
            "name": "세방매점",
            "addr": "경북 경주시 산업로 4447 (용강동 753-1)",
            "lat": 35.876583,
            "lng": 129.226646,
            "pov": {"id": "1165999460", "pan": 284.39, "tilt": 7.27, "zoom": 1}
        },
        {
            "search_name": "세븐일레븐광양시청점",
            "name": "세븐일레븐광양시청점",
            "addr": "전남 광양시 공영로 90 (중동 1317-4)",
            "lat": 34.941465,
            "lng": 127.696615,
            "pov": {"id": "1205208119", "pan": 326.32, "tilt": 16.17, "zoom": -3}
        },
        {
            "search_name": "세븐일레븐화성봉담수기점",
            "name": "세븐일레븐화성봉담수기점",
            "addr": "경기 화성시 세자로 358 (수기리 7-30)",
            "lat": 37.197539,
            "lng": 126.983573,
            "pov": {"id": "1197741392", "pan": 144.33, "tilt": 2.04, "zoom": 1}
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
                    match = True
                elif shop["name"][:3] in name:
                    # Address based matching for shortened names
                    if "세류" in shop["name"] and "세류" in addr and "권선" in addr:
                        match = True
                    elif "세방" in shop["name"] and ("용강" in addr or "경주" in addr):
                        match = True
                    elif "세븐일레븐" in shop["name"] and ("광양" in addr or "화성" in addr):
                        if "광양" in shop["name"] and "광양" in addr: match = True
                        if "봉담" in shop["name"] and "화성" in addr: match = True
                
                if match:
                    # Exclude unrelated shops like "베이스 로또"
                    if "베이스" in name:
                        continue
                        
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
    register_batch_16()
