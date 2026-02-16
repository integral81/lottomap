import json

# Load data
with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Update rules
updates = [
    {
        'name': '팡팡복권마트.잡화슈퍼',
        'addr': '전북 전주시 덕진구',
        'pov': {
            'id': '1171843142',
            'pan': 346.83,
            'tilt': 0.74,
            'zoom': 0
        }
    },
    {
        'name': '대광복권방',
        'addr': '전남 화순군 칠충로',
        'pov': {
            'id': '1192902741',
            'pan': 341.85,
            'tilt': -0.82,
            'zoom': 0
        }
    },
    {
        'name': '행운복권방',
        'addr': '서울 은평구 서오릉로',
        'pov': {
            'id': '1197941920',
            'pan': 38.14,
            'tilt': 3.00,
            'zoom': -2
        }
    },
    {
        'name': '행운복권방',
        'addr': '충북 청주시 상당구',
        'pov': {
            'id': '1169848476',
            'pan': 64.57,
            'tilt': 3.30,
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
