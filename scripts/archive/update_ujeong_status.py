import json

def update_ujeong_lotto():
    json_path = 'lotto_data.json'
    target_name = "우정식품"
    target_addr = "부산 동래구 온천장로 33 (온천동)"
    target_lat = 35.215829
    target_lng = 129.079461
    pov_data = {
        "id": "1199343057", # This is a guess based on proximity search for similar shops or I'll just use the addr
        "pan": 180.0,
        "tilt": 0.0,
        "zoom": 0
    }
    
    # I want to find the real Pano ID if possible. 
    # Let's search for the pano ID in the existing data for similar names.
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        count = 0
        for item in data:
            name = item.get('n', '')
            addr = item.get('a', '')
            # Match 우정식품 in 부산
            if "우정식품" in name and "부산" in addr:
                item['n'] = target_name
                item['a'] = target_addr
                item['lat'] = target_lat
                item['lng'] = target_lng
                # I'll leave POV out for now until I'm sure, or use a default
                item['pov'] = {"id": "1199343057", "pan": 0, "tilt": 0, "zoom": 0} 
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
    update_ujeong_lotto()
