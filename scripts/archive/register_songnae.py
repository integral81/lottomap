import json

def register_songnae():
    json_path = 'lotto_data.json'
    target_name = "송내매표소"
    target_addr = "경기 부천시 소사구 송내1동 709-2"
    target_lat = 37.486887
    target_lng = 126.752854
    pov_data = {
        "id": "1203623206",
        "pan": 275.8,
        "tilt": -2.2,
        "zoom": 0
    }
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        count = 0
        for item in data:
            name = item.get('n', '')
            addr = item.get('a', '')
            
            if target_name in name:
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
    register_songnae()
