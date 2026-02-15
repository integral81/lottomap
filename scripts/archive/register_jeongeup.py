
import json

target_name = "베스트올수성점"
target_addr_parts = ["수성동 932-1", "수성2로 28"]

pov_data = {
    "id": "1183495369",
    "pan": 147.87,
    "tilt": -0.01,
    "fov": 40
}

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updated_count = 0
    for item in data:
        name = item.get('n', '')
        addr = item.get('a', '')
        
        name_match = ("베스트올" in name and "수성" in name)
        addr_match = any(part in addr for part in target_addr_parts)
        
        if name_match and addr_match:
            item['pov'] = pov_data
            updated_count += 1
            
    if updated_count > 0:
        with open('lotto_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Successfully updated {updated_count} entries for {target_name}.")
    else:
        print(f"No matching shop found for {target_name}.")

except Exception as e:
    print(f"Error: {e}")
