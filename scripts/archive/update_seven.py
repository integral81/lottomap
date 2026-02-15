
import json

target_name = "세븐일레븐 홍익"
target_addr = "종합운동장로 161"

new_lat = 37.012518809669736
new_lng = 127.32615404319613
new_pov = {
    "id": "1176123645",
    "pan": 325.0,
    "tilt": 1.0,
    "fov": 40
}

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updated_count = 0
    for item in data:
        name = item.get('n', '')
        addr = item.get('a', '')
        
        # Broad name match + partial address match
        if ("세븐일레븐" in name and "홍익" in name) and target_addr in addr:
            item['lat'] = new_lat
            item['lng'] = new_lng
            item['pov'] = new_pov
            updated_count += 1
            
    if updated_count > 0:
        with open('lotto_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Successfully updated {updated_count} entries for {target_name}.")
    else:
        print(f"No matching shop found for {target_name} at {target_addr}.")

except Exception as e:
    print(f"Error: {e}")
