
import json

target_name = "로터리편의마트"
target_addr_parts = ["포항", "덕산동", "243-9", "서동로 85"]

new_lat = 36.040612035338
new_lng = 129.36719076182058
new_pov = {
    "id": "1187245248",
    "pan": 338.2,
    "tilt": 5.4,
    "fov": 40  # default zoom
}

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updated_count = 0
    for item in data:
        name_match = (target_name in item.get('n', ''))
        addr_match = any(part in item.get('a', '') for part in target_addr_parts)
        
        if name_match and addr_match:
            item['lat'] = new_lat
            item['lng'] = new_lng
            item['pov'] = new_pov
            updated_count += 1
            
    if updated_count > 0:
        with open('lotto_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Successfully updated {updated_count} entries for {target_name}.")
    else:
        print(f"No matching shop found for {target_name} at the specified address.")
except Exception as e:
    print(f"Error: {e}")
