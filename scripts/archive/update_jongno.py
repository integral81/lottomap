
import json

target_name_part = "3가1호선역2번출구"
target_addr_part = "종로3가 23"

new_lat = 37.57069474589658
new_lng = 126.99213511231241
new_pov = {
    "id": "1198163888",
    "pan": 247.5,
    "tilt": 6.0,
    "fov": 40
}

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updated_count = 0
    for item in data:
        name = item.get('n', '')
        addr = item.get('a', '')
        
        # Match by name part and address part
        if target_name_part in name and ("종로" in addr or "3가" in addr):
            item['lat'] = new_lat
            item['lng'] = new_lng
            item['pov'] = new_pov
            updated_count += 1
            
    if updated_count > 0:
        with open('lotto_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Successfully updated {updated_count} entries for 종로3가 가로판매점.")
    else:
        print("No matching shops found.")

except Exception as e:
    print(f"Error: {e}")
