import json

def register_singanpan():
    json_path = 'lotto_data.json'
    target_name = "신간판"
    target_addr = "서울 중구 무교동 12-1"
    target_lat = 37.568103
    target_lng = 126.979480
    pov_data = {
        "id": "1198684037",
        "pan": 76.5,
        "tilt": -7.4,
        "zoom": 0
    }
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        count = 0
        for item in data:
            name = item.get('n', '')
            addr = item.get('a', '')
            
            # Match by name and location
            if "신간판" in name and ("중구" in addr or "무교동" in addr):
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
    register_singanpan()
