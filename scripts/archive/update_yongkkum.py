
import json

target_name = "용꿈돼지꿈복권방"
target_addr_parts = ["하중로 235", "하중동 873-3"]

new_lat = 37.39077062305843
new_lng = 126.80628798120038
new_pov = {
    "id": "1175674861",
    "pan": 54.4,
    "tilt": -4.8,
    "fov": 40
}

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updated_count = 0
    for item in data:
        name = item.get('n', '')
        addr = item.get('a', '')
        
        # Broad match
        if ("용꿈" in name and "돼지꿈" in name) and any(part in addr for part in target_addr_parts):
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
