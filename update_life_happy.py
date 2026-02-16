import json

# Load data
with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Update rules
updates = [
    {
        'name': '라이프마트',
        'addr': '인천 중구 연안부두로53번길',
        'pov': {
            'id': '1198808461',
            'pan': 299.75,
            'tilt': 9.65,
            'zoom': 0
        }
    },
    {
        'name': '행복충전소',
        'addr': '경기 평택시 청북읍',
        'pov': {
            'id': '1203387256',
            'pan': 4.34,
            'tilt': 6.08,
            'zoom': 1
        }
    }
]

# Update
count = 0
updated_names = []
for item in data:
    for update in updates:
        if update['name'] in item['n'] and update['addr'] in item['a']:
            item['pov'] = update['pov']
            count += 1
            if update['name'] not in updated_names:
                updated_names.append(update['name'])

# Save
with open('lotto_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'Updated {count} records')
for name in updated_names:
    print(f'- {name}')
