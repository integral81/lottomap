
import json

target_name = "세븐일레븐"
target_addr = "종합운동장로 161"

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    matches = []
    for item in data:
        if (target_name in item.get('n', '')) and (target_addr in item.get('a', '')):
            matches.append(item)
    
    print(f"Found {len(matches)} matches.")
    for m in matches:
        print(json.dumps(m, ensure_ascii=False))
except Exception as e:
    print(f"Error: {e}")
