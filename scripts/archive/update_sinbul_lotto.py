
import json

target_name = "신불당로또"
target_addr_part = "불당21로 40"

new_lat = 36.81303934802173
new_lng = 127.10525708848067
new_pov = {
    "id": "1195220181",
    "pan": 128.5,
    "tilt": -0.0,
    "fov": 40
}

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updated_count = 0
    for item in data:
        if target_name in item.get('n', '') and target_addr_part in item.get('a', ''):
            item['lat'] = new_lat
            item['lng'] = new_lng
            item['pov'] = new_pov
            updated_count += 1
            
    if updated_count > 0:
        with open('lotto_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Successfully updated {updated_count} entries for {target_name}.")
    else:
        print(f"No matching shop found for {target_name}.")

except Exception as e:
    print(f"Error: {e}")
