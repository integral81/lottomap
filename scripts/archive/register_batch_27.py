import json

def register_batch_27():
    json_path = 'lotto_data.json'
    
    # Shop Data for Batch 27
    batch_data = [
        {
            "search_name": "좋은터",
            "name": "좋은터",
            "addr": "인천 계양구 효서로 204 (효성동)",
            "lat": 37.527816,
            "lng": 126.718550,
            "pov": {"id": "1199148045", "pan": 188.59, "tilt": -1.94, "zoom": -3}
        },
        {
            "search_name": "주몽동명",
            "name": "주몽동명",
            "addr": "경기 용인시 수지구 중앙공원로 319 (풍덕천동)",
            "lat": 37.315684,
            "lng": 127.087658,
            "pov": {"id": "1199630767", "pan": 323.96, "tilt": 0.23, "zoom": 3}
        },
        {
            "search_name": "중구-가로가판대-37",
            "name": "중구-가로가판대-37",
            "addr": "서울 중구 남대문로 20-2 (남대문로3가)",
            "lat": 37.560831,
            "lng": 126.978063,
            "pov": {"id": "1198730080", "pan": 161.69, "tilt": 5.99, "zoom": 0}
        },
        {
            "search_name": "중흥마트",
            "name": "중흥마트",
            "addr": "광주 북구 문산로 30 (문흥동)",
            "lat": 35.184059,
            "lng": 126.922488,
            "pov": {"id": "1200655927", "pan": 112.15, "tilt": -1.08, "zoom": 0}
        },
        {
            "search_name": "진동에이스점",
            "name": "지에스(GS)25 진동에이스점",
            "addr": "경남 창원시 마산합포구 진동면 해양관광로 49",
            "lat": 35.116008,
            "lng": 128.486404,
            "pov": {"id": "1205302792", "pan": 9.53, "tilt": 9.36, "zoom": 0}
        },
        {
            "search_name": "지에스25 신매태왕점로또",
            "name": "지에스25 신매태왕점로또",
            "addr": "대구 수성구 욱수천로 70 (신매동)",
            "lat": 35.834511,
            "lng": 128.711612,
            "pov": {"id": "1201352672", "pan": 139.44, "tilt": 7.28, "zoom": 0}
        },
        {
            "search_name": "진대박",
            "name": "진대박 로또복권방",
            "addr": "울산 동구 대송로 139 (화정동)",
            "lat": 35.495669,
            "lng": 129.423103,
            "pov": {"id": "1202150969", "pan": 100.16, "tilt": 6.84, "zoom": 0}
        },
        {
            "search_name": "진도로또",
            "name": "진도로또",
            "addr": "전남 진도군 진도읍 남동길 15-2",
            "lat": 34.481294,
            "lng": 126.269289,
            "pov": {"id": "1189129866", "pan": 154.44, "tilt": 1.56, "zoom": 0}
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
                        if shop["search_name"] == "중흥마트" and "광주" not in addr: continue
                        if shop["search_name"] == "진도로또" and "진도" not in addr: continue
                        match = True
                elif ("남대문로" in addr or "30-6" in addr) and shop["search_name"] == "중구-가로가판대-37":
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
    register_batch_27()
