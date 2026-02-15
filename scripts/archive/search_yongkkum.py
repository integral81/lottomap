
import json

target_name = "용꿈돼지꿈복권방"
target_addr_part = "하중로 235"

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    matches = []
    for item in data:
        if (target_name in item.get('n', '')) or (target_addr_part in item.get('a', '')):
            matches.append(item)
    
    print(f"Found {len(matches)} matches.")
    for m in matches:
        print(json.dumps(m, ensure_ascii=False))
except Exception as e:
    print(f"Error: {e}")
