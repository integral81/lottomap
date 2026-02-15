
import json

target_name = "수퍼복권대박"
target_addr = "용담로 60"

new_lat = 37.418817980032394
new_lng = 126.67373696197622
new_pov = {
    "id": "1200644068",
    "pan": 204.6,
    "tilt": -6.0,
    "fov": 40
}

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updated_count = 0
    for item in data:
        # Broad match for name
        if target_name in item.get('n', '') and target_addr in item.get('a', ''):
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
