import json

def register_token_sales():
    json_path = 'lotto_data.json'
    target_name = "토큰판매"
    target_addr = "경북 경산시 대학로 291 토큰박스 (대동 168-1)"
    target_lat = 35.8373
    target_lng = 128.7538
    pov_data = {
        "id": "1186505662",
        "pan": 226.1,
        "tilt": 0.0,
        "zoom": 0
    }
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        count = 0
        for item in data:
            name = item.get('n', '')
            addr = item.get('a', '')
            # Match "토큰판매" or "토큰박스" in Gyeongsan
            if ("토큰판매" in name or "토큰박스" in name) and "경산" in addr:
                item['n'] = target_name
                item['a'] = target_addr
                item['lat'] = target_lat
                item['lng'] = target_lng
                item['pov'] = pov_data
                if 'closed' in item:
                    del item['closed']
                count += 1
                
        if count > 0:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Successfully updated {count} records in lotto_data.json for {target_name}.")
        else:
            print("No matching records found in lotto_data.json.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    register_token_sales()
