
import json

target_name = "베스트올수성점"
target_addr = "수성동 932-1"

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    matches = []
    for item in data:
        if (target_name in item.get('n', '')) or (target_addr in item.get('a', '')):
            matches.append(item)
    
    print(f"Found {len(matches)} matches.")
    for m in matches[:5]:
        print(json.dumps(m, ensure_ascii=False))
except Exception as e:
    print(f"Error: {e}")
