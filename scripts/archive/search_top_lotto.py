
import json

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    matches = []
    for item in data:
        if "탑로또" in item.get('n', ''):
            matches.append(item)
    
    print(f"Found {len(matches)} matches for '탑로또'.")
    for m in matches:
        print(json.dumps(m, ensure_ascii=False))

except Exception as e:
    print(f"Error: {e}")
