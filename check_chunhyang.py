import json

f_json = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json'

with open(f_json, 'r', encoding='utf-8') as f:
    data = json.load(f)

print("Checking for '춘향' or '남원'...")
matches = [s for s in data if ('춘향' in s.get('n', '') or '남원' in s.get('a', ''))]

for m in matches:
    print(f"Name: {m.get('n')}")
    print(f"Addr: {m.get('a')}")
    print(f"Wins: {m.get('wins', 0)}")
    print(f"POV: {m.get('pov')}")
    print("-" * 20)
