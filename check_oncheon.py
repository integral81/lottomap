import json

with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for s in data:
    if "세븐일레븐부산온천장역점" in s.get('n', ''):
        print(f"Name: {s['n']}")
        print(f"Address: {s['a']}")
        print(f"POV: {s.get('pov')}")
        print(f"Custom Message: {s.get('customMessage', 'None')}")
        print("-" * 20)
