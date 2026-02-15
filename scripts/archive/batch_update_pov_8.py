
import json

updates = [
    {
        "name": "진우복권",
        "search_n": "진우복권",
        "search_a": "월드컵대로 119",
        "pov": {"id": "1202681433", "pan": 140.36, "tilt": -14.43, "fov": 110}
    },
    {
        "name": "진우행운복권방",
        "search_n": "진우행운복권방",
        "search_a": "도척로 327",
        "pov": {"id": "1202782769", "pan": 274.51, "tilt": -5.46, "fov": 110}
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
