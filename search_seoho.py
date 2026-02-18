import json
path = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Search for any mention of '서호동'
results = [s for s in data if '서호동' in s.get('a', '')]
results.sort(key=lambda x: x['r'], reverse=True)

for s in results:
    print(f"{s['r']}rd: {s['n']} ({s['a']})")
