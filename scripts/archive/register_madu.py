
import json

target_name = "마두5번출구가판로또"
target_addr_part = "마두동 801-1"

pov_data = {
    "id": "1203614423",
    "pan": 65.84,
    "tilt": -1.57,
    "fov": 40  # Default FOV for zoom 1 or similar
}

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updated_count = 0
    for item in data:
        name = item.get('n', '')
        addr = item.get('a', '')
        
        # Broad match for "마두" and "5번출구" in name
        name_match = ("마두" in name and "5번출구" in name)
        # Match either address variant
        addr_match = ("마두동 801-1" in addr) or ("중앙로 1200" in addr) or ("802-1" in addr)

        if name_match and addr_match:
            item['pov'] = pov_data
            updated_count += 1
            
    if updated_count > 0:
        with open('lotto_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Successfully updated {updated_count} entries for {target_name}.")
    else:
        print(f"No matching shop found for {target_name} at the specified address.")
except Exception as e:
    print(f"Error: {e}")
