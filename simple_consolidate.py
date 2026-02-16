import json

# Load data
with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Consolidation rules
rules = [
    {
        'name': '복권나라',
        'main': '인천 남구 용현동 611-1',
        'merge': ['인천 미추홀구 토금북로 47']
    },
    {
        'name': '25시슈퍼',
        'main': '경기 시흥시 정왕동 1882-11번지 홍익프라자1층107호',
        'merge': ['함송로14번길 13-17']
    },
    {
        'name': '로또복권방',
        'main': '세종 용포로 32',
        'merge': ['세종 금남면 용포리 85-1']
    }
]

# Get main coordinates
main_coords = {}
for rule in rules:
    for item in data:
        if item['n'] == rule['name'] and item['a'] == rule['main']:
            main_coords[rule['name']] = {
                'lat': item['lat'],
                'lng': item['lng']
            }
            break

# Consolidate
count = 0
for item in data:
    for rule in rules:
        if item['n'] == rule['name'] and item['a'] in rule['merge']:
            item['a'] = rule['main']
            if rule['name'] in main_coords:
                item['lat'] = main_coords[rule['name']]['lat']
                item['lng'] = main_coords[rule['name']]['lng']
            count += 1

# Save
with open('lotto_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'Consolidated {count} records')
