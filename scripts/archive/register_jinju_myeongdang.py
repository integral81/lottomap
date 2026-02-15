
import json

target_name = "명당"
target_addr_part = "동부로 1356"

pov_data = {
    "id": "1193074745",
    "pan": 103.35,
    "tilt": -1.22,
    "fov": 30  # Adjusted for zoom 2
}

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updated_count = 0
    for item in data:
        name = item.get('n', '')
        addr = item.get('a', '')
        
        # Match for "명당" in name and "동부로 1356" in address to avoid other "명당" shops
        if target_name in name and target_addr_part in addr:
            item['pov'] = pov_data
            updated_count += 1
            
    if updated_count > 0:
        with open('lotto_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Successfully updated {updated_count} entries for {target_name} at {target_addr_part}.")
    else:
        print(f"No matching shop found for {target_name} at {target_addr_part}.")

except Exception as e:
    print(f"Error: {e}")
