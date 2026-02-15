import json

lotto_data_path = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json"

targets = [
    {"name": "복권나라", "hint": "포항"},
    {"name": "복권나라", "hint": "원주"},
    {"name": "복권나라", "hint": "증평"}
]

with open(lotto_data_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for target in targets:
    print(f"Searching for: {target['name']} ({target['hint']})")
    matches = [e for e in data if target['name'] in e.get('n', '') and target['hint'] in e.get('a', '')]
    print(f"Found {len(matches)} wins:")
    for m in matches:
        print(f"  Round {m['r']}: {m['a']}")
    print("-" * 20)
