import json

def register_happy_ppl_legend():
    json_path = 'lotto_data.json'
    target_name = "행복한사람들 (흥부네)"
    # Standardizing to the most famous "명당" address
    target_addr = "경기 광주시 곤지암읍 경충대로 763 (삼리 399-18)"
    target_lat = 37.351930
    target_lng = 127.323580
    pov_data = {
        "id": "1203636282",
        "pan": 210.3,
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
            
            # Match variants: "행복한사람들", "흥부네", "흥부네복권방" etc. in Gwangju
            match = False
            if ("행복한사람들" in name or "흥부네" in name) and "광주" in addr:
                match = True
            
            if match:
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
    register_happy_ppl_legend()
