import json

f_json = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json'

with open(f_json, 'r', encoding='utf-8') as f:
    data = json.load(f)

search_names = ['Goodday', '완월로또', '채널큐', '해피복권', '도소매복권방', '옥좌로또점']

for name in search_names:
    print(f"--- Search: {name} ---")
    matches = [s for s in data if name in s.get('n', '')]
    for m in matches:
        print(f"  Name: {m.get('n')}")
        print(f"  Addr: {m.get('a')}")
        print(f"  Wins: {m.get('wins', 1)}")
        print(f"  POV: {m.get('panoid')}")
        print("-" * 20)
