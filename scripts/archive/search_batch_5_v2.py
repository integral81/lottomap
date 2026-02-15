
import json

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    matches = []
    for item in data:
        if "우일" in item.get('n', '') and ("송파" in item.get('a', '') or "마천" in item.get('a', '')):
            matches.append(item)
    print(f"Found {len(matches)} matches for 우일 (Songpa/Macheon).")
    for m in matches:
        print(json.dumps(m, ensure_ascii=False))

except Exception as e:
    print(f"Error: {e}")
