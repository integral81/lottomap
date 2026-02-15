
import json

shops_to_update = [
    { "name": "성호복권방", "addr": "신일동로 1", "pov": { "id": "1163152394", "pan": 147.13, "tilt": 10.93, "fov": 110 } },
    { "name": "세종로또방", "addr": "용포로 32", "pov": { "id": "1200677283", "pan": 71.08, "tilt": 7.72, "fov": 110 } }
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
