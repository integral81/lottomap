import json

def register_investigation_cases():
    json_path = 'lotto_data.json'
    
    cases = [
        {
            "search_name": "일이오마켓", # Also known as 이리오마켓
            "name": "일이오마켓",
            "addr": "서울 서초구 방배동 454-20 1층 (효령로34길 7)",
            "lat": 37.481515,
            "lng": 126.997232,
            "pov": {"id": "1050437224", "pan": 205.3, "tilt": 0.0, "zoom": 0},
            "region": "서초"
        },
        {
            "search_name": "훼미리마트", # Rebranded to CU Yeoju IC
            "name": "CU(여주IC점)",
            "addr": "경기 여주시 세종로 390 (점봉동 437-11)",
            "lat": 37.266213,
            "lng": 127.632064,
            "pov": {"id": "1174827365", "pan": 321.8, "tilt": 0.0, "zoom": 0},
            "region": "여주"
        }
    ]
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        for case in cases:
            count = 0
            for item in data:
                name = item.get('n', '')
                addr = item.get('a', '')
                
                # Match logic
                match = False
                if case["search_name"][:3] in name and case["region"] in addr:
                    match = True
                # Special check for Family Mart -> CU transition win records
                if case["name"] == "CU(여주IC점)" and "훼미리" in name and "여주" in addr:
                    match = True
                
                if match:
                    item['n'] = case["name"]
                    item['a'] = case["addr"]
                    item['lat'] = case["lat"]
                    item['lng'] = case["lng"]
                    item['pov'] = case["pov"]
                    if 'closed' in item:
                        del item['closed'] 
                    count += 1
            print(f"Updated {count} records for {case['name']}.")
            
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    register_investigation_cases()
