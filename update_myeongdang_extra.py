
import json

# Load data
with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Update rules
updates = [
    {
        'name': '복권명당',
        'addr': '경기 안산시 단원구',
        'pov': {
            'id': '1204138025',
            'pan': 174.64,
            'tilt': 4.11,
            'zoom': -1
        }
    },
    {
        'name': '복권명당',
        'addr': '경기 안성시 승두길',
        'pov': {
            'id': '1176200480',
            'pan': 153.53,
            'tilt': -2.24,
            'zoom': -1
        }
    },
    {
        'name': '복권명당',
        'addr': '경북 구미시 상사동로',
        'pov': {
            'id': '1165753417',
            'pan': 350.64,
            'tilt': -5.52,
            'zoom': -3
        }
    },
    {
        'name': '복권명당',
        'addr': '충북 청주시 상당구',
        'pov': {
            'id': '1170004964',
            'pan': 241.72,
            'tilt': -3.20,
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
            entry_name = f"{item['n']} ({item['a']})"
            if entry_name not in updated_names:
                updated_names.append(entry_name)

# Save
with open('lotto_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'Updated {count} records')
for name in updated_names:
    print(f'- {name}')
