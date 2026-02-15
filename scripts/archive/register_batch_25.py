import json

def register_batch_25():
    json_path = 'lotto_data.json'
    
    # Shop Data for Batch 25
    batch_data = [
        {
            "search_name": "잉크와복권방",
            "name": "잉크와복권방",
            "addr": "충남 천안시 동남구 산단로 84 (신방동)",
            "lat": 36.802077,
            "lng": 127.139416,
            "pov": {"id": "1195017651", "pan": 157.82, "tilt": 7.48, "zoom": -2}
        },
        {
            "search_name": "장군슈퍼",
            "name": "장군슈퍼",
            "addr": "경기 부천시 오정구 삼작로 837 (고강동)",
            "lat": 37.530954,
            "lng": 126.805135,
            "pov": {"id": "1203452762", "pan": 286.75, "tilt": 9.48, "zoom": -2}
        },
        {
            "search_name": "제일복권",
            "name": "제일복권",
            "addr": "경남 양산시 양산역2길 7 (중부동)",
            "lat": 35.335572,
            "lng": 129.027956,
            "pov": {"id": "1204952001", "pan": 20.08, "tilt": 2.68, "zoom": -2}
        },
        {
            "search_name": "제일슈퍼",
            "name": "제일슈퍼",
            "addr": "인천 연수구 앵고개로 937 (동춘동)",
            "lat": 37.408630,
            "lng": 126.670837,
            "pov": {"id": "1199991356", "pan": 302.10, "tilt": 8.91, "zoom": -3}
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
                        if shop["search_name"] == "잉크와복권방" and "천안" not in addr: continue
                        if shop["search_name"] == "장군슈퍼" and "부천" not in addr: continue
                        if shop["search_name"] == "제일복권" and "양산" not in addr: continue
                        if shop["search_name"] == "제일슈퍼" and "연수" not in addr: continue
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
    register_batch_25()
