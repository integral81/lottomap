
import json

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    matches = []
    for item in data:
        name = item.get('n', '')
        if "마두" in name and "5번출구" in name:
            matches.append(item)
    
    print(f"Found {len(matches)} matches.")
    for m in matches:
        print(json.dumps(m, ensure_ascii=False))
except Exception as e:
    print(f"Error: {e}")
