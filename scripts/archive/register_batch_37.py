import json

def register_batch_37():
    json_path = 'lotto_data.json'
    
    batch_data = [
        {
            "search_name": "흥건슈퍼",
            "name": "흥건슈퍼",
            "addr": "전북 전주시 완산구 거마평로 25 (삼천동1가 300-3)",
            "lat": 35.794734,
            "lng": 127.116660,
            "pov": {"id": "1172135927", "pan": 246.28, "tilt": -0.33, "zoom": 0},
            "region": "전주"
        },
        {
            "search_name": "희망복권방",
            "name": "희망복권방",
            "addr": "전남 나주시 풍물시장1길 3 (이창동 759-3)",
            "lat": 34.992633,
            "lng": 126.709467,
            "pov": {"id": "1191106973", "pan": 221.94, "tilt": 5.47, "zoom": 0},
            "region": "나주"
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
                if shop["search_name"][:2] in name and shop["region"] in addr:
                     # Specific check for Naju to avoid "Hope Lotto" etc if exists
                     if shop["name"] == "희망복권방" and "나주" not in addr:
                         continue
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
    register_batch_37()
