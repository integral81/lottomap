import json

def register_jinbin():
    json_path = 'lotto_data.json'
    target_name = "진빈레코드"
    target_addr = "경남 밀양시 북성로 7"
    target_lat = 35.498458
    target_lng = 128.743849
    pov_data = {
        "id": "1187794818",
        "pan": 344.1,
        "tilt": -0.8,
        "zoom": 0
    }
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        count = 0
        for item in data:
            name = item.get('n', '')
            addr = item.get('a', '')
            
            # Match 진빈/Miryang
            if "진빈" in name and "밀양" in addr:
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
    register_jinbin()
