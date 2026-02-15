
import json

target_name = "신영슈퍼"
target_addr_part = "광평로51길 27"

new_lat = 37.4886384231356
new_lng = 127.10175165950983
new_pov = {
    "id": "1016761294",
    "pan": 155.0,
    "tilt": -4.7,
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
