
import json

target_name = "버스표가판점"
target_addr_part = "호계동 1039-2"

pov_data = {
    "id": "1203300471",
    "pan": 238.48,
    "tilt": -1.77,
    "fov": 30  # Adjusted for zoom 2
}

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updated_count = 0
    for item in data:
        name = item.get('n', '')
        addr = item.get('a', '')
        
        # Match for "버스표가판점" and address part
        if target_name in name and target_addr_part in addr:
            item['pov'] = pov_data
            updated_count += 1
            
    if updated_count > 0:
        with open('lotto_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Successfully updated {updated_count} entries for {target_name} at {target_addr_part}.")
    else:
        # Fallback broad match for name if address variant exists
        updated_count = 0
        for item in data:
            if target_name in item.get('n', ''):
                item['pov'] = pov_data
                updated_count += 1
        
        if updated_count > 0:
            with open('lotto_data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Successfully updated {updated_count} entries for {target_name} via broad name match.")
        else:
            print(f"No matching shop found for {target_name}.")

except Exception as e:
    print(f"Error: {e}")
