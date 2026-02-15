import json

def register_batch_23():
    json_path = 'lotto_data.json'
    
    # Shop Data for Batch 23
    batch_data = [
        {
            "search_name": "원동슈퍼",
            "name": "원동슈퍼",
            "addr": "충남 보령시 중앙로 151 (대천동)",
            "lat": 36.351188,
            "lng": 126.597412,
            "pov": {"id": "1176675568", "pan": 87.41, "tilt": 9.90, "zoom": -3}
        },
        {
            "search_name": "원스탑",
            "name": "원스탑",
            "addr": "서울 송파구 백제고분로7길 39 (잠실동)",
            "lat": 37.510968,
            "lng": 127.083235,
            "pov": {"id": "1197972849", "pan": 75.93, "tilt": 3.81, "zoom": -3}
        },
        {
            "search_name": "월드 복권방",
            "name": "월드 복권방",
            "addr": "서울 강서구 곰달래로53길 41 (화곡동)",
            "lat": 37.533515,
            "lng": 126.858791,
            "pov": {"id": "1198750232", "pan": 230.34, "tilt": 0.14, "zoom": -3}
        },
        {
            "search_name": "월드마트",
            "name": "월드마트",
            "addr": "충북 청주시 흥덕구 복대동 2405",
            "lat": 36.624777,
            "lng": 127.447669,
            "pov": {"id": "1170655642", "pan": 349.33, "tilt": -1.31, "zoom": -3}
        },
        {
            "search_name": "유방매표소",
            "name": "유방매표소",
            "addr": "경기 용인시 처인구 백옥대로 1388 (유방동)",
            "lat": 37.258839,
            "lng": 127.212952,
            "pov": {"id": "1199301411", "pan": 80.98, "tilt": 0.86, "zoom": -1}
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
                    region = shop["addr"].split()[0]
                    if region in addr:
                        # Extra filters to avoid false positives
                        if shop["search_name"] == "원동슈퍼" and "보령" not in addr: continue
                        if shop["search_name"] == "원스탑" and "송파" not in addr: continue
                        if shop["search_name"] == "월드 복권방" and "강서" not in addr: continue
                        if shop["search_name"] == "월드마트" and "청주" not in addr: continue
                        if shop["search_name"] == "유방매표소" and "용인" not in addr: continue
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
    register_batch_23()
