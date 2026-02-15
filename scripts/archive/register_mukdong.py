
import json

target_name = "묵동식품"
target_addr = "동일로 919"

pov_data = {
    "id": "1198448343",
    "pan": 217.73,
    "tilt": 1.91,
    "fov": 30  # Estimated fov for zoom 3
}

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updated_count = 0
    for item in data:
        name = item.get('n', '')
        addr = item.get('a', '')
        
        if target_name in name and target_addr in addr:
            item['pov'] = pov_data
            updated_count += 1
            
    if updated_count > 0:
        with open('lotto_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Successfully updated {updated_count} entries for {target_name}.")
    else:
        # Try broader match if failed
        updated_count = 0
        for item in data:
            if target_name in item.get('n', ''):
                item['pov'] = pov_data
                updated_count += 1
        
        if updated_count > 0:
            with open('lotto_data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Successfully updated {updated_count} entries for {target_name} via broad match.")
        else:
            print(f"No matching shop found for {target_name}.")

except Exception as e:
    print(f"Error: {e}")
