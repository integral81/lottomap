import json

def finalize_ujeong_lotto():
    json_path = 'lotto_data.json'
    target_name = "우정식품"
    target_addr = "부산 동래구 온천장로 33 (온천동)"
    target_lat = 35.215829
    target_lng = 129.079461
    pov_data = {
        "id": "1199343057",
        "pan": 0,
        "tilt": 0,
        "zoom": 0
    }
    
    new_record_1191 = {
        "r": 1191,
        "n": target_name,
        "a": target_addr,
        "m": "자동",
        "lat": target_lat,
        "lng": target_lng,
        "pov": pov_data
    }
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # 1. Check if 1191 exists
        exists_1191 = any(item.get('r') == 1191 and item.get('n') == target_name for item in data)
        if not exists_1191:
            data.append(new_record_1191)
            print("Added record for Round 1191.")
            
        # 2. Consolidate all records
        count = 0
        for item in data:
            if "우정식품" in item.get('n', '') and "부산" in item.get('a', ''):
                item['n'] = target_name
                item['a'] = target_addr
                item['lat'] = target_lat
                item['lng'] = target_lng
                item['pov'] = pov_data
                if 'closed' in item:
                    del item['closed']
                count += 1
                
        # Sort data by round (optional but good for consistency)
        data.sort(key=lambda x: x['r'], reverse=True)
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully finalized {count} records in lotto_data.json for {target_name}.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    finalize_ujeong_lotto()
