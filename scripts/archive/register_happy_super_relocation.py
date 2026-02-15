import json

def register_happy_super_relocation():
    json_path = 'lotto_data.json'
    target_name = "행복슈퍼"
    target_addr = "서울 성북구 동소문로 49 (동소문동4가 115)"
    target_lat = 37.591021
    target_lng = 127.011144
    pov_data = {
        "id": "1198249504",
        "pan": 326.8,
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
            
            # Match "행복슈퍼" in Seongbuk (both old and new addresses)
            if "행복슈퍼" in name and "성북" in addr:
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
            print(f"Successfully consolidated {count} records in lotto_data.json for {target_name}.")
        else:
            print("No matching records found in lotto_data.json.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    register_happy_super_relocation()
