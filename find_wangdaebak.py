import json

with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=== Search Results for '왕대박' ===")
for s in data:
    if '왕대박' in s['n']:
        print(f"{s['n']} | {s['a']}")
