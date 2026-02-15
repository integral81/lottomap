import json

def register_terminafood():
    json_path = 'lotto_data.json'
    target_name = "터미널식품"
    target_addr = "경기 의정부시 의정로 640 (금오동 369-5)"
    target_lat = 37.745465
    target_lng = 127.055081
    pov_data = {
        "id": "1174621645",
        "pan": 108.1,
        "tilt": 1.0,
        "zoom": 0
    }
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        count = 0
        for item in data:
            name = item.get('n', '')
            addr = item.get('a', '')
            
            # Match "터미널식품" in Uijeongbu
            if "터미널식품" in name and "의정부" in addr:
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
    register_terminafood()
