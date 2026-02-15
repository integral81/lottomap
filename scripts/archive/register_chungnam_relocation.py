import json

def register_chungnam_relocation():
    json_path = 'lotto_data.json'
    target_name = "충남상회"
    target_addr = "인천 미추홀구 참외전로 268 302동 B211호 (숭의동)"
    # New Coordinates (from R1168)
    target_lat = 37.467642
    target_lng = 126.643012
    pov_data = {
        "id": "1199530667",
        "pan": 121.4,
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
            # Match 충남상회 in Incheon
            if "충남상회" in name and "인천" in addr:
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
    register_chungnam_relocation()
