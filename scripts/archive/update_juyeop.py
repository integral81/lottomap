
import json

target_name = "주엽역"
target_addr_part = "중앙로 1437"

new_lat = 37.670181206504616
new_lng = 126.76090977959345
new_pov = {
    "id": "1203613079",
    "pan": 200.1,
    "tilt": -2.1,
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
