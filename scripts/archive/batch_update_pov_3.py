
import json

shops_to_update = [
    { "name": "부영마트", "addr": "상봉동 108", "pov": { "id": "1198489183", "pan": 89.74, "tilt": 2.29, "fov": 40 } },
    { "name": "부자복권방", "addr": "대명동 138-12", "pov": { "id": "1172510553", "pan": 49.56, "tilt": 1.59, "fov": 40 } },
    { "name": "빙그레 돈벼락 맞는곳", "addr": "병동리 980-7", "pov": { "id": "1194446892", "pan": 194.70, "tilt": -2.33, "fov": 40 } },
    { "name": "삼삼마트", "addr": "봉곡동 27-3", "pov": { "id": "1192627362", "pan": 176.85, "tilt": -0.72, "fov": 40 } },
    { "name": "서재강변로또", "addr": "서재리 58-2", "pov": { "id": "1200883300", "pan": 117.79, "tilt": 4.16, "fov": 40 } }
]

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total_updated = 0
    for shop in shops_to_update:
        updated_count = 0
        for item in data:
            # Broad name match + partial address match
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
