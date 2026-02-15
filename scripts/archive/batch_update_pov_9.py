
import json

shops_to_update = [
    { "name": "천하명당", "addr": "탄현로 224", "pov": { "id": "1198300869", "pan": 88.97, "tilt": 2.77, "fov": 40 } },
    { "name": "천하명당복권", "addr": "칠곡중앙대로 545", "pov": { "id": "1201202732", "pan": 279.85, "tilt": -0.62, "fov": 110 } },
    { "name": "천하명당복권", "addr": "관음동 1249-4", "pov": { "id": "1201464298", "pan": 216.31, "tilt": -2.18, "fov": 110 } },
    { "name": "천하명당복권방", "addr": "매산로 2", "pov": { "id": "1200112677", "pan": 54.08, "tilt": -2.08, "fov": 110 } },
    { "name": "탑로또", "addr": "상동동 979-1", "pov": { "id": "1204692322", "pan": 204.23, "tilt": 2.01, "fov": 110 } },
    { "name": "팡팡복권방", "addr": "광혜원리 265-3", "pov": { "id": "1185181825", "pan": 143.99, "tilt": 4.43, "fov": 110 } }
]

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total_updated = 0
    for shop in shops_to_update:
        updated_count = 0
        for item in data:
            # Match by name and partial address
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
