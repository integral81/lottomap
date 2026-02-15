
import json

target_name = "원당역복권방"
# URL location
new_lat = 37.65401690279633
new_lng = 126.84180143646313
new_pov = {
    "id": "1203875563",
    "pan": 47.7,
    "tilt": 7.5,
    "fov": 40
}

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updated_count = 0
    for item in data:
        if target_name in item.get('n', ''):
            # Update all entries for this shop to the confirmed URL location
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
