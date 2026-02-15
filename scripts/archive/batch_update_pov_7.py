
import json

shops_to_update = [
    { "name": "종합복권방", "addr": "해리 189-2", "pov": { "id": "1189205617", "pan": 191.96, "tilt": 2.12, "fov": 110 } },
    { "name": "주택복권방", "addr": "우산초교길 29", "pov": { "id": "1195999144", "pan": 202.48, "tilt": -6.97, "fov": 110 } },
    { "name": "주택복권방", "addr": "풍덕천동 717-3", "pov": { "id": "1199750330", "pan": 134.22, "tilt": 5.86, "fov": 40 } }
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
