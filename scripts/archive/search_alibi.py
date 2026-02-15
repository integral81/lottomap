
import json

target_name = "알리바이"
target_addr_part = "신가동 986-4"

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    matches = []
    for item in data:
        if target_name in item.get('n', '') and ("광산구" in item.get('a', '') or target_addr_part in item.get('a', '')):
            matches.append(item)
    
    print(f"Found {len(matches)} matches for {target_name} in Gwangju Gwangsan-gu.")
    for m in matches[:5]:
        print(json.dumps(m, ensure_ascii=False))
except Exception as e:
    print(f"Error: {e}")
