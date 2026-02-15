import json

def register_batch_19():
    json_path = 'lotto_data.json'
    
    # Shop Data for Batch 19
    batch_data = [
        {
            "search_name": "씨유제주 제일점",
            "name": "씨유제주 제일점",
            "addr": "제주 제주시 신산로 16 CU 제일점",
            "lat": 33.511909,
            "lng": 126.531441,
            "pov": {"id": "1182173481", "pan": 295.36, "tilt": 0.35, "zoom": -1}
        },
        {
            "search_name": "아띠로또판매점",
            "name": "아띠로또판매점",
            "addr": "충남 천안시 서북구 두정동 1063 레몬타워 110호",
            "lat": 36.837256,
            "lng": 127.134072,
            "pov": {"id": "1195351579", "pan": 42.24, "tilt": 6.75, "zoom": -1}
        },
        {
            "search_name": "안성휴게소 복권판매점(부산방향)",
            "name": "안성휴게소 복권판매점(부산방향)",
            "addr": "경기 안성시 경부고속도로 365 (안성휴게소 하행선)",
            "lat": 37.013582,
            "lng": 127.144716,
            "pov": {"id": "1178222520", "pan": 221.72, "tilt": -0.87, "zoom": -3}
        },
        {
            "search_name": "양산덕계점(로또)",
            "name": "양산덕계점(로또)",
            "addr": "경남 양산시 평산동 94-4 미니스톱평산점내",
            "lat": 35.381908,
            "lng": 129.151348,
            "pov": {"id": "1204744414", "pan": 105.68, "tilt": 7.90, "zoom": -3}
        },
        {
            "search_name": "에버빌마트",
            "name": "에버빌마트",
            "addr": "경북 안동시 정하동 240-2",
            "lat": 36.551121,
            "lng": 128.731261,
            "pov": {"id": "1166518651", "pan": 325.95, "tilt": 4.87, "zoom": -1}
        },
        {
            "search_name": "엘도라도복권점문점",
            "name": "엘도라도복권점문점",
            "addr": "서울 광진구 중곡동 124-65",
            "lat": 37.557823,
            "lng": 127.087620,
            "pov": {"id": "1198573579", "pan": 270.34, "tilt": 7.47, "zoom": -3}
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
                    # Additional region check to be safe
                    region = shop["addr"].split()[0]
                    if region in addr or region[:2] in addr:
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
    register_batch_19()
