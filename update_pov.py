import json

# Load data
with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Update rules
updates = [
    {
        'name': '황금복권방',
        'addr': '부산 부산진구 가야대로',
        'pov': {
            'id': '1202246843',
            'pan': 344.72,
            'tilt': -0.29,
            'zoom': -1
        }
    },
    {
        'name': '로또휴게실',
        'addr': '경기 용인시 기흥구',
        'pov': {
            'id': '1199447820',
            'pan': 282.00,
            'tilt': 1.20,
            'zoom': 0
        }
    }
]

# Update
count = 0
for item in data:
    for update in updates:
        if update['name'] in item['n'] and update['addr'] in item['a']:
            item['pov'] = update['pov']
            count += 1

# Save
with open('lotto_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'Updated {count} records')
print('')
print('황금복권방: PanoID 1202246843 (pan: 344.72, tilt: -0.29, zoom: -1)')
print('로또휴게실: PanoID 1199447820 (pan: 282.00, tilt: 1.20, zoom: 0)')
