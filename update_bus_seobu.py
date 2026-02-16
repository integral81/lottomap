import json

# Load data
with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Update rules
updates = [
    {
        'name': '버스표판매소',
        'addr': '경기 고양시 덕양구',
        'pov': {
            'id': '1203599818',
            'pan': 277.18,
            'tilt': 15.08,
            'zoom': -3
        }
    },
    {
        'name': '복권명당(서부점)',
        'addr': '대구 달서구 월배로',
        'pov': {
            'id': '1201394989',
            'pan': 135.73,
            'tilt': -0.29,
            'zoom': -3
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
