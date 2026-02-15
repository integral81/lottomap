import json

with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Correct address from user image: 경북 문경시 중앙로 15 1층
count = 0
for s in data:
    if '왕대박' in s['n'] and '문경' in s['a']:
        s['a'] = "경북 문경시 중앙로 15 1층"
        count += 1

with open('lotto_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Final Fix: Updated {count} records in lotto_data.json to '중앙로 15 1층'")
