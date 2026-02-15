import json

def register_taean_relocation():
    json_path = 'lotto_data.json'
    target_name = "태안로또복권방"
    target_addr = "충남 태안군 태안읍 독샘로 57 1층"
    # New Coordinates
    target_lat = 36.753488
    target_lng = 126.298530
    pov_data = {
        "id": "1161074841",
        "pan": 187.1,
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
            # Match 태안로또 in Taean
            if "태안로또" in name and "태안" in addr:
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
            print(f"Successfully updated {count} records in lotto_data.json for {target_name} at new location.")
        else:
            print("No matching records found in lotto_data.json.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    register_taean_relocation()
