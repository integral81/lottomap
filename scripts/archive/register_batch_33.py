import json

def register_batch_33():
    json_path = 'lotto_data.json'
    
    # Shop Data for Batch 33
    batch_data = [
        {
            "search_name": "하이로또",
            "name": "하이로또",
            "addr": "서울 금천구 금하로 686 (시흥동 908-2)",
            "lat": 37.451900,
            "lng": 126.906355,
            "pov": {"id": "1198115190", "pan": 207.07, "tilt": -0.75, "zoom": -3}
        },
        {
            "search_name": "하프타임(괴정점)",
            "name": "하프타임(괴정점)",
            "addr": "부산 사하구 사하로 156 (괴정동 282-3)",
            "lat": 35.102431,
            "lng": 128.997999,
            "pov": {"id": "1202279089", "pan": 190.40, "tilt": 9.30, "zoom": -3}
        },
        {
            "search_name": "학동복권나라",
            "name": "학동복권나라",
            "addr": "전남 여수시 흥국로 6 (학동 69-2)",
            "lat": 34.763569,
            "lng": 127.663464,
            "pov": {"id": "1205447251", "pan": 184.53, "tilt": 6.00, "zoom": -2}
        },
        {
            "search_name": "한경종합광고",
            "name": "한경종합광고",
            "addr": "서울 송파구 백제고분로 198 (삼전동 28-8)",
            "lat": 37.503937,
            "lng": 127.088562,
            "pov": {"id": "1197947148", "pan": 229.72, "tilt": -3.46, "zoom": 1}
        },
        {
            "search_name": "한국인세계대박복권",
            "name": "한국인세계대박복권",
            "addr": "인천 연수구 독배로197번길 34 (옥련동 285)",
            "lat": 37.427719,
            "lng": 126.655242,
            "pov": {"id": "1200648163", "pan": 243.73, "tilt": 8.21, "zoom": 1}
        },
        {
            "search_name": "한마음",
            "name": "한마음",
            "addr": "서울 관악구 은천로 211 봉천중앙시장 라열 4호 (봉천동 32-2)",
            "lat": 37.484186,
            "lng": 126.954467,
            "pov": {"id": "1198387489", "pan": 40.92, "tilt": 3.54, "zoom": -3}
        },
        {
            "search_name": "한아름매점",
            "name": "한아름매점",
            "addr": "충남 홍성군 광천읍 광천로 330 (광천리 173-6)",
            "lat": 36.503246,
            "lng": 126.625567,
            "pov": {"id": "1160927350", "pan": 8.10, "tilt": -0.76, "zoom": -3}
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
    register_batch_33()
