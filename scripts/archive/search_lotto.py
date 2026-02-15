
import json

target_name = "로터리"
target_addr = "포항"

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    matches = []
    for item in data:
        if (target_name in item.get('n', '')) or (target_addr in item.get('a', '')):
            matches.append(item)
    
    print(f"Found {len(matches)} matches.")
    for m in matches[:10]:
        print(m)
except Exception as e:
    print(f"Error: {e}")
