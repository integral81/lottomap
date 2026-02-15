import json

def register_unsoo_cheonan():
    json_path = 'lotto_data.json'
    target_name = "운수대통복권방"
    target_addr = "충남 천안시 동남구 대흥로 122 중앙시장 입구"
    # Correct Cheonan coordinates for 대흥로 122
    target_lat = 36.800537
    target_lng = 127.149245
    pov_data = {
        "id": "1194931057",
        "pan": 15.4,
        "tilt": -2.4,
        "zoom": 0
    }
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        count = 0
        for item in data:
            name = item.get('n', '')
            addr = item.get('a', '')
            
            # Match 운수대통 in 천안
            if "운수대통" in name and "천안" in addr:
                # Extra check to avoid 수원 운수대통 (already registered)
                if "수원" in addr:
                    continue
                
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
            print(f"Successfully updated {count} records in lotto_data.json for {target_name} (Cheonan).")
        else:
            print("No matching records found in lotto_data.json.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    register_unsoo_cheonan()
