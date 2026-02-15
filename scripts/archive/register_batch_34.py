import json

def register_batch_34():
    json_path = 'lotto_data.json'
    
    # Shop Data for Batch 34
    batch_data = [
        {
            "search_name": "행복한복권방",
            "name": "행복한복권방",
            "addr": "전북 전주시 덕진구 가리내로 50 (서신동 770-1)",
            "lat": 35.8458,
            "lng": 127.1124,
            "pov": {"id": "1205157999", "pan": 275.76, "tilt": -0.04, "zoom": -3},
            "region": "전주"
        },
        {
            "search_name": "행복한집",
            "name": "행복한집",
            "addr": "경기 오산시 성호대로 105 (원동 345-42)",
            "lat": 37.1472,
            "lng": 127.0754,
            "pov": {"id": "1174616837", "pan": 190.15, "tilt": 0.65, "zoom": -3},
            "region": "오산"
        },
        {
            "search_name": "행운 마트",
            "name": "행운 마트",
            "addr": "인천 남동구 만수로 73 (만수동 895-35)",
            "lat": 37.4526,
            "lng": 126.7329,
            "pov": {"id": "1198840880", "pan": 181.10, "tilt": -0.66, "zoom": -1},
            "region": "인천"
        },
        {
            "search_name": "행운나라복권방",
            "name": "행운나라복권방",
            "addr": "경기 안양시 만안구 안양로 279 (안양동 622-167)",
            "lat": 37.3948,
            "lng": 126.9247,
            "pov": {"id": "1203012551", "pan": 161.53, "tilt": 4.44, "zoom": -3},
            "region": "안양"
        },
        {
            "search_name": "행운로또",
            "name": "행운로또",
            "addr": "경기 김포시 약암로 911 (대곶면 약암리 395-2)",
            "lat": 37.6015,
            "lng": 126.5416,
            "pov": {"id": "1203919081", "pan": 256.26, "tilt": 7.75, "zoom": -2},
            "region": "김포"
        },
        {
            "search_name": "행운로또복권",
            "name": "행운로또복권",
            "addr": "경기 오산시 경기대로 213 (오산동 854-32)",
            "lat": 37.1486,
            "lng": 127.0673,
            "pov": {"id": "1174497959", "pan": 183.58, "tilt": -5.70, "zoom": -3},
            "region": "오산"
        },
        {
            "search_name": "행운의집제1호점",
            "name": "행운의집제1호점",
            "addr": "경북 안동시 경동로 663 (동부동 75-3)",
            "lat": 36.5651,
            "lng": 128.7333,
            "pov": {"id": "1166526789", "pan": 82.96, "tilt": 2.57, "zoom": -2},
            "region": "안동"
        },
        {
            "search_name": "행운편의점",
            "name": "행운편의점",
            "addr": "광주 북구 면앙로 36 (두암동 597-4)",
            "lat": 35.1794,
            "lng": 126.9161,
            "pov": {"id": "1200322797", "pan": 188.93, "tilt": 4.19, "zoom": -2},
            "region": "광주"
        },
        {
            "search_name": "혁신대박",
            "name": "혁신대박",
            "addr": "충북 음성군 맹동면 원중로 1434 103호 (두성리 1461)",
            "lat": 36.9095,
            "lng": 127.5411,
            "pov": {"id": "1165317318", "pan": 32.07, "tilt": -0.06, "zoom": -2},
            "region": "음성"
        },
        {
            "search_name": "현대슈퍼",
            "name": "현대슈퍼",
            "addr": "광주 서구 상무대로 871 (쌍촌동 970-24)",
            "lat": 35.1505,
            "lng": 126.8573,
            "pov": {"id": "1204198971", "pan": 355.65, "tilt": -1.05, "zoom": -2},
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
                
                # Matching
                match = False
                if shop["search_name"][:3] in name and shop["region"] in addr:
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
    register_batch_34()
