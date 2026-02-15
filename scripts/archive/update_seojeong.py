
import json

target_name = "서정천하명당"
target_addr_parts = ["서정동 262-11", "서정역로 160"]

new_lat = 37.058204268145445
new_lng = 127.05921493127471
new_pov = {
    "id": "1198410230",
    "pan": 72.8,
    "tilt": 0.7,
    "fov": 40
}

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updated_count = 0
    for item in data:
        name = item.get('n', '')
        
        if target_name in name:
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
