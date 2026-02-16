
import json

with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

update = {
    'name': '행운복권방',
    'addr': '경기 수원시 영통구',
    'pov': {
        'id': '1199461361',
        'pan': 134.71,
        'tilt': 0.48,
        'zoom': -2
    }
}

count = 0
for item in data:
    if update['name'] in item['n'] and update['addr'] in item['a']:
        item['pov'] = update['pov']
        count += 1

with open('lotto_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Updated {count} records for Haengun Lottery (Suwon)")
