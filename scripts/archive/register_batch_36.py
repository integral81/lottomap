import json

def register_batch_36():
    json_path = 'lotto_data.json'
    
    batch_data = [
        {
            "search_name": "홈돌이로또복권",
            "name": "홈돌이로또복권",
            "addr": "경기 김포시 중봉1로 14 (감정동 692)",
            "lat": 37.623847,
            "lng": 126.698608,
            "pov": {"id": "1203881568", "pan": 88.57, "tilt": 2.32, "zoom": -3},
            "region": "김포"
        },
        {
            "search_name": "화천복권방",
            "name": "화천복권방",
            "addr": "강원 화천군 화천읍 중앙로 14 (하리 43-28)",
            "lat": 38.104946,
            "lng": 127.704488,
            "pov": {"id": "1195567514", "pan": 132.19, "tilt": 8.41, "zoom": -3},
            "region": "화천"
        },
        {
            "search_name": "황금대박점",
            "name": "황금대박점",
            "addr": "서울 노원구 공릉로 328 (하계동 117)",
            "lat": 37.635999,
            "lng": 127.071027,
            "pov": {"id": "1197986427", "pan": 65.96, "tilt": 4.66, "zoom": 0},
            "region": "서울"
        },
        {
            "search_name": "황금로또",
            "name": "황금로또",
            "addr": "부산 동구 중앙대로251번길 42-1 (초량동 251-10)",
            "lat": 35.120165,
            "lng": 129.039605,
            "pov": {"id": "1202438640", "pan": 357.79, "tilt": 4.87, "zoom": 0},
            "region": "부산"
        },
        {
            "search_name": "황금복권",
            "name": "황금복권",
            "addr": "강원 원주시 천사로 74 (단계동 808)",
            "lat": 37.351183,
            "lng": 127.929520,
            "pov": {"id": "1195748262", "pan": 68.33, "tilt": -1.33, "zoom": 0},
            "region": "원주"
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
                
                # Match logic
                match = False
                if shop["search_name"][:2] in name:
                    if shop["region"] in addr or shop["region"] in name:
                        # Extra check for Wonju "황금복권" to distinguishing from others
                        if shop["name"] == "황금복권" and "단계" not in addr and "천사로" not in addr:
                             continue
                        match = True
                
                if match:
                    item['n'] = shop["name"]
                    item['a'] = shop["addr"]
                    item['lat'] = shop["lat"]
                    item['lng'] = shop["lng"]
                    item['pov'] = shop["pov"]
                    if 'closed' in item:
                        del item['closed'] # Re-open if marked closed
                    count += 1
            print(f"Updated {count} records for {shop['name']}.")
            
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    register_batch_36()
