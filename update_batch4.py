import json

# Load data
with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Update rules
updates = [
    {
        'name': '또또복권방',
        'addr': '전북 익산시 고봉로32길',
        'pov': {
            'id': '1179975833',
            'pan': 5.12,
            'tilt': 6.07,
            'zoom': -1
        }
    },
    {
        'name': '현대장미슈퍼',
        'addr': '전북 익산시 동서로61길',
        'pov': {
            'id': '1179925999',
            'pan': 236.67,
            'tilt': 3.66,
            'zoom': -1
        }
    },
    {
        'name': '갈렙분식한식',
        'addr': '서울 중랑구 용마산로115길',
        'pov': {
            'id': '1198253759',
            'pan': 106.99,
            'tilt': -2.05,
            'zoom': -3
        }
    },
    {
        'name': '공원슈퍼',
        'addr': '경기 수원시 장안구',
        'pov': {
            'id': '1199575474',
            'pan': 337.38,
            'tilt': 2.61,
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
