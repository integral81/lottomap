import json

def register_happy_lotto():
    json_path = 'lotto_data.json'
    target_name = "행복로또판매점"
    target_addr = "경기 의정부시 오목로 219 106호 (민락동 812-3)"
    target_lat = 37.745876
    target_lng = 127.099401
    pov_data = {
        "id": "1174312490",
        "pan": 291.6,
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
            
            # Match "행복로또" in Uijeongbu
            if "행복로또" in name and "의정부" in addr:
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
    register_happy_lotto()
