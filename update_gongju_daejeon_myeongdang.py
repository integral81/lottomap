
import json

# Load data
with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Update rules
updates = [
    {
        'name': '복권명당',
        'addr': '충남 공주시 번영1로',
        'pov': {
            'id': '1179373419',
            'pan': 312.66,
            'tilt': 0.23,
            'zoom': -2
        }
    },
    {
        'name': '복권명당',
        'addr': '대전 중구 목중로',
        'pov': {
            'id': '1201428533',
            'pan': 215.44,
            'tilt': 2.95,
            'zoom': -2
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
