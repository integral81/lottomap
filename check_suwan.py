import json

f_json = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json'

with open(f_json, 'r', encoding='utf-8') as f:
    data = json.load(f)

print("Checking '세븐일레븐 수완점'...")
matches = [s for s in data if '세븐일레븐' in s.get('n', '') and '수완' in s.get('n', '')]

if not matches:
    print("No exact match found. Searching address...")
    matches = [s for s in data if '수완동' in s.get('a', '') and '1428' in s.get('a', '')]

for m in matches:
    print(f"Name: {m.get('n')}")
    print(f"Addr: {m.get('a')}")
    print(f"Wins: {m.get('wins', 0)}")
    print(f"Closed: {m.get('closed', False)}")
    print("-" * 20)
