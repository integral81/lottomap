import json

f_json = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json'

with open(f_json, 'r', encoding='utf-8') as f:
    data = json.load(f)

targets = [
    { "name": "복권판매소", "addr": "국채보상로 438" },
    { "name": "청구마트", "addr": "검단로 34" },
    { "name": "월드복권", "addr": "북비산로 98" },
    { "name": "대흥당", "addr": "관통로 102" }
]

print("Checking for duplicates...")
for t in targets:
    matches = [s for s in data if (t['name'] in s.get('n', '') and t['addr'] in s.get('a', ''))]
    print(f"Target: {t['name']} ({t['addr']}) - Found {len(matches)} matches")
    for m in matches:
        print(f"  - {m.get('n')} | {m.get('a')} | Wins: {m.get('wins', 0)} | POV: {m.get('pov') is not None}")
    print("-" * 30)
