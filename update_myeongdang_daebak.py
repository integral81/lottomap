
import json

# Load data
with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Update rules
updates = [
    {
        'name': '복권명당',
        'addr': '경북 경주시 동문로',
        'pov': {
            'id': '1187226622',
            'pan': 83.17,
            'tilt': -2.25,
            'zoom': -3
        }
    },
    {
        'name': '대박행진 복권랜드',
        'addr': '경기 파주시 금빛로',
        'pov': {
            'id': '1045548538',
            'pan': 177.36,
            'tilt': 7.04,
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
