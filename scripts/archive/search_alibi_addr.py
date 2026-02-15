
import json

target_addr = "신가동 986-4"

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    matches = []
    for item in data:
        if target_addr in item.get('a', ''):
            matches.append(item)
    
    print(f"Found {len(matches)} matches for address {target_addr}.")
    for m in matches:
        print(json.dumps(m, ensure_ascii=False))
except Exception as e:
    print(f"Error: {e}")
