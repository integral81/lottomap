
import json

# Load data
with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Update rules
updates = [
    {
        'name': '복권명당',
        'addr': '대구 동구 경안로',
        'pov': {
            'id': '1201246324',
            'pan': 265.87,
            'tilt': 7.53,
            'zoom': -3
        }
    },
    {
        'name': '복권명당',
        'addr': '대구 수성구 천을로',
        'pov': {
            'id': '1201275541',
            'pan': 207.87,
            'tilt': 1.44,
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
