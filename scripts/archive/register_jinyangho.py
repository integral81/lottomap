import json

def register_jinyangho():
    json_path = 'lotto_data.json'
    target_name = "진양호"
    target_addr = "경남 진주시 남강로 58 (신안동)"
    target_lat = 35.162807
    target_lng = 128.048415
    pov_data = {
        "id": "1205317765",
        "pan": 227.1,
        "tilt": 4.8,
        "zoom": 0
    }
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        count = 0
        for item in data:
            name = item.get('n', '')
            addr = item.get('a', '')
            
            # Match "진양호" or "e마트24(진양호)" in "진주"
            if ("진양호" in name or "e마트24" in name) and "진주" in addr:
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
    register_jinyangho()
