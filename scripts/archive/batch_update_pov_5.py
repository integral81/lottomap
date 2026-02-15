
import json

updates = [
    {
        "name": "왕대박복권방",
        "search_n": "왕대박",
        "search_a": "모전동",
        "pov": {"id": "1184892306", "pan": 321.11, "tilt": -2.73, "fov": 110}
    },
    {
        "name": "우일",
        "search_n": "우일",
        "search_a": "마천",
        "pov": {"id": "1198540869", "pan": 30.76, "tilt": 0.70, "fov": 40}
    }
]

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total_updated = 0
    for up in updates:
        count = 0
        for item in data:
            if up["search_n"] in item.get('n', '') and up["search_a"] in item.get('a', ''):
                item['pov'] = up["pov"]
                count += 1
        print(f"Updated {count} entries for {up['name']}")
        total_updated += count

    if total_updated > 0:
        with open('lotto_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Successfully finished batch update. Total: {total_updated}")

except Exception as e:
    print(f"Error: {e}")
