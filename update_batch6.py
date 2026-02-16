
import json

# Load data
with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Update rules
updates = [
    {
        'name': '북마산복권전문점',
        'addr': '경남 창원시 마산합포구',
        'pov': {
            'id': '1204481175',
            'pan': 86.04,
            'tilt': 1.92,
            'zoom': -3
        }
    },
    {
        'name': '복권전문점',
        'addr': '인천 부평구 원적로',
        'pov': {
            'id': '1199144048',
            'pan': 346.51,
            'tilt': 7.56,
            'zoom': -3
        }
    },
    {
        'name': '복권전문점',
        'addr': '경기 시흥시 중심상가로',
        'pov': {
            'id': '1176040887',
            'pan': 221.10,
            'tilt': -1.89,
            'zoom': -3
        }
    },
    {
        'name': '복권전문점',
        'addr': '대전 유성구 봉명동',
        'pov': {
            'id': '1201068426',
            'pan': 208.99,
            'tilt': 5.62,
            'zoom': -3
        }
    },
    {
        'name': '월드24시',
        'addr': '서울 은평구 통일로',
        'pov': {
            'id': '1197925499',
            'pan': 157.52,
            'tilt': -5.65,
            'zoom': -3
        }
    },
    {
        'name': '영광정보통신',
        'addr': '서울 성북구 화랑로',
        'pov': {
            'id': '1197958742',
            'pan': 121.39,
            'tilt': -0.73,
            'zoom': -1
        }
    },
    {
        'name': '천하명당복권방',
        'addr': '충남 홍성군 홍성읍',
        'pov': {
            'id': '1161022469',
            'pan': 190.82,
            'tilt': 2.23,
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
            entry_name = f"{item['n']} ({item['a']})"
            if entry_name not in updated_names:
                updated_names.append(entry_name)

# Save
with open('lotto_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'Updated {count} records')
for name in updated_names:
    print(f'- {name}')
