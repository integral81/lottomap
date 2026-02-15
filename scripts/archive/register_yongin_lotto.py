import json

def register_yongin_lotto():
    json_path = 'lotto_data.json'
    target_name = "용인로또복권방"
    target_addr = "경기 용인시 처인구 백옥대로 2076-1 101호"
    target_lat = 37.310273
    target_lng = 127.240582
    pov_data = {
        "id": "1198462052",
        "pan": 253.3,
        "tilt": 2.3,
        "zoom": 0
    }
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        count = 0
        for item in data:
            name = item.get('n', '')
            addr = item.get('a', '')
            
            # Match 용인로또 in 용인
            if "용인로또" in name and "용인" in addr:
                item['n'] = target_name
                item['a'] = target_addr
                item['lat'] = target_lat
                item['lng'] = target_lng
                item['pov'] = pov_data
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
    register_yongin_lotto()
