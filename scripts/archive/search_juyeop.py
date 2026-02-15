
import json

target_name = "주엽역"
target_addr = "중앙로 1437"

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    matches = []
    for item in data:
        if target_name in item.get('n', '') and (target_addr in item.get('a', '') or "주엽동" in item.get('a', '')):
            matches.append(item)
    
    print(f"Found {len(matches)} matches for '{target_name}' in Goyang.")
    for m in matches:
        print(json.dumps(m, ensure_ascii=False))

except Exception as e:
    print(f"Error: {e}")
