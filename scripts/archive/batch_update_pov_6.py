
import json

shops_to_update = [
    { "name": "인생대역전", "addr": "임학동 10-10", "pov": { "id": "1198902079", "pan": 313.09, "tilt": -3.24, "fov": 110 } },
    { "name": "일등복권편의점", "addr": "본리동 2-16", "pov": { "id": "1201526676", "pan": 345.04, "tilt": 6.19, "fov": 110 } },
    { "name": "자수정슈퍼", "addr": "효자동1가 195-19", "pov": { "id": "1172061409", "pan": 143.45, "tilt": 2.03, "fov": 40 } },
    { "name": "제이복권방", "addr": "종로5가 58", "pov": { "id": "1197815068", "pan": 359.17, "tilt": -3.40, "fov": 40 } }
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
