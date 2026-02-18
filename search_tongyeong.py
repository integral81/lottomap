import json
import os

path = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

tongyeong_wins = [s for s in data if '통영' in s.get('a', '')]
tongyeong_wins.sort(key=lambda x: x['r'], reverse=True)

for s in tongyeong_wins:
    print(f"{s['r']}rd: {s['n']} ({s['a']})")
