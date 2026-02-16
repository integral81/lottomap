import json

# Load data
with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Update rules
updates = [
    {
        'name': '명당골복권방',
        'addr': '경기 수원시 권선구',
        'pov': {
            'id': '1199752151',
            'pan': 17.38,
            'tilt': 2.96,
            'zoom': -1
        }
    },
    {
        'name': '천하명당복권방',
        'addr': '경남 거제시 옥포성안로',
        'pov': {
            'id': '1204368034',
            'pan': 86.04,
            'tilt': -2.09,
            'zoom': -1
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
