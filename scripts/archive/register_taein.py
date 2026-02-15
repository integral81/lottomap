import json

def register_taein():
    json_path = 'lotto_data.json'
    target_name = "태인(금돼지) 복권"
    target_addr = "경기 성남시 분당구 돌마로 85 제105호 (금곡동)"
    target_lat = 37.350388
    target_lng = 127.111343
    pov_data = {
        "id": "1199347895",
        "pan": 227.4,
        "tilt": 6.7,
        "zoom": 0
    }
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        count = 0
        for item in data:
            name = item.get('n', '')
            addr = item.get('a', '')
            
            # Match "태인" in Bundang/Seongnam
            if "태인" in name and ("성남" in addr or "분당" in addr):
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
    register_taein()
