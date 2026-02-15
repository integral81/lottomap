import json

def register_batch_15():
    json_path = 'lotto_data.json'
    
    # Shop Data
    batch_data = [
        {
            "search": "새상무복권",
            "name": "새상무복권",
            "addr": "광주 서구 치평로 30 (상무중앙빌딩)",
            "lat": 35.149950,
            "lng": 126.847670,
            "pov": {"id": "1200264569", "pan": 84.89, "tilt": -4.64, "zoom": -3}
        },
        {
            "search": "서울구가-17가판",
            "name": "서울구가-17가판",
            "addr": "서울 구로구 구로동로 130-2 (구로시장입구)",
            "lat": 37.490325,
            "lng": 126.884395,
            "pov": {"id": "1198161548", "pan": 53.34, "tilt": -3.18, "zoom": -3}
        },
        {
            "search": "서울로또방",
            "name": "서울로또방",
            "addr": "충북 옥천군 삼금로 8 (옥천읍)",
            "lat": 36.299390,
            "lng": 127.566719,
            "pov": {"id": "1185003403", "pan": 119.43, "tilt": -0.34, "zoom": -3}
        },
        {
            "search": "서해로또방",
            "name": "서해로또방",
            "addr": "경기 화성시 화성로 1471 (남양읍)",
            "lat": 37.223209,
            "lng": 126.842336,
            "pov": {"id": "1196541229", "pan": 353.7, "tilt": 11.64, "zoom": -2}
        },
        {
            "search": "성강동인",
            "name": "성강동인",
            "addr": "경기 하남시 신장로 212 (신장동)",
            "lat": 37.543922,
            "lng": 127.198273,
            "pov": {"id": "1173491031", "pan": 53.61, "tilt": 0.16, "zoom": -3}
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
                # Ensure we match the correct shop (especially for common names like '서울로또방')
                if shop["search"] in name or (shop["addr"].split()[0] in addr and shop["name"][:3] in name):
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
    register_batch_15()
