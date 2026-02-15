import json

def register_batch_20():
    json_path = 'lotto_data.json'
    
    # Shop Data for Batch 20
    batch_data = [
        {
            "search_name": "여기있었네복권방",
            "name": "여기있었네복권방",
            "addr": "전북 김제시 남북로 171",
            "lat": 35.799391,
            "lng": 126.884571,
            "pov": {"id": "1182321361", "pan": 291.33, "tilt": 4.14, "zoom": -3}
        },
        {
            "search_name": "열두보석복권방",
            "name": "열두보석복권방",
            "addr": "경기 용인시 기흥구 구갈동 351 구갈스포츠센터 106호",
            "lat": 37.281144,
            "lng": 127.111825,
            "pov": {"id": "1199898636", "pan": 175.83, "tilt": 3.67, "zoom": -3}
        },
        {
            "search_name": "영훈슈퍼마켓",
            "name": "영훈슈퍼마켓",
            "addr": "서울 도봉구 창3동 557-5",
            "lat": 37.637808,
            "lng": 127.037690,
            "pov": {"id": "1173492955", "pan": 128.01, "tilt": 8.12, "zoom": -3}
        },
        {
            "search_name": "예술로또",
            "name": "예술로또",
            "addr": "강원 영월군 영월읍 영흥리 945-43",
            "lat": 37.183339,
            "lng": 128.468483,
            "pov": {"id": "1196180027", "pan": 171.52, "tilt": 8.57, "zoom": -1}
        },
        {
            "search_name": "예스복권방",
            "name": "예스복권방",
            "addr": "경기 남양주시 별내중앙로 56 메인프라자 1층 105호",
            "lat": 37.647555,
            "lng": 127.123738,
            "pov": {"id": "1202966955", "pan": 72.76, "tilt": 5.83, "zoom": -1}
        },
        {
            "search_name": "온천로또복권",
            "name": "온천로또복권",
            "addr": "충남 예산군 덕산면 사동리 15 (덕산온천관광호텔 매점)",
            "lat": 35.960663,
            "lng": 128.931668,
            "pov": {"id": "1200482286", "pan": 163.74, "tilt": 6.10, "zoom": -3}
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
                    # Region check to avoid false positives (e.g., Namyangju vs Cheonan for Yes Lotto)
                    region = shop["addr"].split()[0] # 전북, 경기, 서울, 강원, 충남
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
    register_batch_20()
