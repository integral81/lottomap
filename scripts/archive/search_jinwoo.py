
import json

shops_to_search = [
    {"n": "진우복권", "a": "월드컵대로 119"},
    {"n": "진우행운복권방", "a": "도척로 327"}
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
