import json

def update_allin_lotto():
    json_path = 'lotto_data.json'
    target_name = "올인로또복권"
    target_addr = "전북 전주시 완산구 효자동2가 203-5 코끼리마트 상가 내"
    pov_data = {
        "id": "1172093455",
        "pan": 343.3,
        "tilt": -2.0,
        "zoom": 0
    }
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        count = 0
        for item in data:
            if target_name in item.get('n', '') and "전주" in item.get('a', ''):
                item['n'] = target_name
                item['a'] = target_addr
                item['pov'] = pov_data
                if 'closed' in item:
                    del item['closed'] # Mark as open
                count += 1
                
        if count > 0:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Successfully updated {count} records for {target_name}.")
        else:
            print(f"No records found for {target_name}.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_allin_lotto()
