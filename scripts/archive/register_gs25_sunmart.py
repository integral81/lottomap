import json

def register_gs25_sunmart():
    json_path = 'lotto_data.json'
    old_name = "썬마트"
    new_name = "GS25 관저신선점"
    target_addr = "대전 서구 관저동 1109 신선타워 105호"
    target_lat = 36.300811
    target_lng = 127.334425
    pov_data = {
        "id": "1200797712",
        "pan": 338.3,
        "tilt": -0.7,
        "zoom": 0
    }
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        count = 0
        for item in data:
            name = item.get('n', '')
            addr = item.get('a', '')
            
            # Match 썬마트 in 관저동 1109
            if old_name in name and ("관저동" in addr or "1109" in addr):
                item['n'] = new_name
                item['a'] = target_addr
                item['lat'] = target_lat
                item['lng'] = target_lng
                item['pov'] = pov_data
                count += 1
                
        if count > 0:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Successfully updated {count} records in lotto_data.json for {new_name}.")
        else:
            print("No matching records found in lotto_data.json.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    register_gs25_sunmart()
