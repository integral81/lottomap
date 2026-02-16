
import json

# Load data
with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Update rules
updates = [
    {
        'name': '천하명당복권방',
        'addr': '서울 송파구 백제고분로41길',
        'pov': {
            'id': '1198700337',
            'pan': 152.45,
            'tilt': 2.62,
            'zoom': -3
        }
    },
    {
        'name': '천하명당복권방',
        'addr': '인천 계양구 안남로',
        'pov': {
            'id': '1199160980',
            'pan': 99.43,
            'tilt': 3.13,
            'zoom': 1
        }
    },
    {
        'name': '천하명당복권방',
        'addr': '서울 광진구 중곡3동',
        'pov': {
            'id': '1198442558',
            'pan': 302.84,
            'tilt': 3.18,
            'zoom': 2
        }
    },
    {
        'name': '천하명당복권방',
        'addr': '경기 안성시 영동',
        'pov': {
            'id': '1176477381',
            'pan': 186.97,
            'tilt': 2.37,
            'zoom': 2
        }
    },
    {
        'name': '천하명당복권방',
        'addr': '경기 화성시 남양동',
        'pov': {
            'id': '1197151995',
            'pan': 310.69,
            'tilt': 2.65,
            'zoom': 0
        }
    },
    {
        'name': '대산슈퍼',
        'addr': '충남 천안시 동남구',
        'pov': {
            'id': '1153043095',
            'pan': 162.89,
            'tilt': 3.06,
            'zoom': 0
        }
    },
    {
        'name': '로또킹',
        'addr': '서울 영등포구 영중로',
        'pov': {
            'id': '1171055517',
            'pan': 4.30,
            'tilt': -2.37,
            'zoom': -2
        }
    },
    {
        'name': '성심상회',
        'addr': '경북 포항시 북구',
        'pov': {
            'id': '1186982437',
            'pan': 165.96,
            'tilt': -4.06,
            'zoom': -2
        }
    },
    {
        'name': '빅세일복권방',
        'addr': '부산 부산진구 서면문화로',
        'pov': {
            'id': '1202698289',
            'pan': 106.42,
            'tilt': 0.24,
            'zoom': 2
        }
    },
    {
        'name': '주택복권방',
        'addr': '경기 안양시 만안구',
        'pov': {
            'id': '1202873895',
            'pan': 139.65,
            'tilt': -0.99,
            'zoom': 1
        }
    },
    {
        'name': '보람복권방',
        'addr': '울산 남구 화합로194번길',
        'pov': {
            'id': '1201998535',
            'pan': 187.13,
            'tilt': 3.20,
            'zoom': -3
        }
    },
    {
        'name': '평안당',
        'addr': '서울 종로구 종로',
        'pov': {
            'id': '1197815101',
            'pan': 321.55,
            'tilt': 2.27,
            'zoom': 2
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
