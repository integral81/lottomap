
import json

target_name = "원당역"

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    matches = []
    for item in data:
        if target_name in item.get('n', ''):
            matches.append(item)
    
    print(f"Found {len(matches)} matches for '{target_name}'.")
    for m in sorted(matches, key=lambda x: x['r'], reverse=True):
        print(json.dumps(m, ensure_ascii=False))

except Exception as e:
    print(f"Error: {e}")
