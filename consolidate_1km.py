import json

# Load data
with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# New consolidation rules (1km radius)
rules = [
    {
        'name': '행운복권방',
        'main': '부산 중구 남포동5가 64-3번지',
        'merge': ['부산 서구 충무동1가 28-19']
    },
    {
        'name': '노다지복권방',
        'main': '서울 종로구 창신동 302-5',
        'merge': ['서울 동대문구 한빛로 1-1', '서울 중구 신당동 110-10']
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

print(f'Consolidated {count} records (1km radius)')
print('')
print('Details:')
print('- 행운복권방: 부산 서구 -> 부산 중구 (705.8m)')
print('- 노다지복권방: 서울 동대문구, 중구 -> 서울 종로구 (914m, 919m)')
