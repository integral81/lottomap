import json

def consolidate_happy_24():
    json_path = 'lotto_data.json'
    target_name = "해피+24시편의점"
    target_addr = "광주 북구 하서로 330 (양산동 296)"
    target_lat = 35.204467
    target_lng = 126.873870
    pov_data = {
        "id": "1200291324",
        "pan": 88.36,
        "tilt": -6.01,
        "zoom": -3
    }
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        count = 0
        for item in data:
            name = item.get('n', '')
            addr = item.get('a', '')
            # Match "해피+24시편의점" in Gwangju Buk-gu
            if "해피+24시편의점" in name and "광주" in addr:
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
            print(f"Successfully consolidated {count} records in lotto_data.json for {target_name}.")
        else:
            print("No matching records found in lotto_data.json.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    consolidate_happy_24()
