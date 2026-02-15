
import json

shops_to_search = [
    {"n": "왕대박", "a": "모전동"},
    {"n": "우일", "a": "마천동"}
]

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for search in shops_to_search:
        matches = []
        for item in data:
            if search["n"] in item.get('n', '') and search["a"] in item.get('a', ''):
                matches.append(item)
        print(f"Found {len(matches)} matches for {search['n']} ({search['a']})")
        for m in matches[:3]:
            print(json.dumps(m, ensure_ascii=False))

except Exception as e:
    print(f"Error: {e}")
