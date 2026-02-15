
import json

shops_to_update = [
    { "name": "복권파는집", "addr": "합성동 84-29", "pov": { "id": "1204721909", "pan": 296.28, "tilt": 0.69, "fov": 40 } },
    { "name": "복돼지복권방", "addr": "3.1만세로 43", "pov": { "id": "1196772296", "pan": 333.88, "tilt": -1.32, "fov": 40 } },
    { "name": "본스튜디오", "addr": "하귀로 111", "pov": { "id": "1181077460", "pan": 328.68, "tilt": 7.12, "fov": 40 } }
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
