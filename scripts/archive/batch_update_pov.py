
import json

shops_to_update = [
    { "name": "복권나라", "addr": "은천로 40-1", "pov": { "id": "1198290120", "pan": 183.53, "tilt": 2.70, "fov": 40 } },
    { "name": "복권마을", "addr": "구로동로 72", "pov": { "id": "1198161436", "pan": 72.08, "tilt": -1.14, "fov": 40 } },
    { "name": "복권방", "addr": "장림동 328-9", "pov": { "id": "1202461052", "pan": 38.69, "tilt": -3.05, "fov": 40 } },
    { "name": "복권세상", "addr": "청호로 139", "pov": { "id": "1192169730", "pan": 217.44, "tilt": 0.44, "fov": 40 } },
    { "name": "복권세상", "addr": "우암로 21-1", "pov": { "id": "1174843105", "pan": 105.59, "tilt": 1.46, "fov": 40 } }
]

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total_updated = 0
    for shop in shops_to_update:
        updated_count = 0
        for item in data:
            if shop["name"] in item.get('n', '') and shop["addr"] in item.get('a', ''):
                item['pov'] = shop["pov"]
                updated_count += 1
        print(f"Updated {updated_count} entries for {shop['name']} ({shop['addr']})")
        total_updated += updated_count
            
    if total_updated > 0:
        with open('lotto_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Successfully updated total {total_updated} entries.")
    else:
        print("No matching shops found.")

except Exception as e:
    print(f"Error: {e}")
