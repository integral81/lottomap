import json
import os
import shutil
from datetime import datetime

# 1. Backup
src_file = 'lotto_data.json'
backup_file = f'lotto_data_backup_batch12_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
shutil.copy(src_file, backup_file)
print(f"Backup created: {backup_file}")

# 2. Load Data
with open(src_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 3. Define Updates
updates = [
    {'name': '청솔서점', 'addr': '부산 사하구', 'pov': {'id': '1161907485', 'pan': 192.09, 'tilt': 4.27, 'zoom': 0}},
    {'name': '대박슈퍼', 'addr': '인천 부평구', 'pov': {'id': '1199058573', 'pan': 193.20, 'tilt': 1.32, 'zoom': 1}},
    {'name': '진평양행', 'addr': '강원 강릉시', 'pov': {'id': '1194087152', 'pan': 148.48, 'tilt': 6.34, 'zoom': -3}},
    {'name': '그린마트', 'addr': '경기 성남시', 'pov': {'id': '1184095310', 'pan': 280.49, 'tilt': 8.63, 'zoom': -3}},
    {'name': '천하명당', 'addr': '경기 시흥시', 'pov': {'id': '1175741918', 'pan': 318.61, 'tilt': -0.87, 'zoom': -3}},
    {'name': '신문가판점', 'addr': '서울 용산구', 'pov': {'id': '1197632088', 'pan': 301.43, 'tilt': -9.47, 'zoom': -3}},
    {'name': '버스매표소', 'addr': '인천 부평구', 'pov': {'id': '1199209059', 'pan': 321.40, 'tilt': -9.03, 'zoom': -3}},
    {'name': '가로판매소', 'addr': '서울 구로구', 'pov': {'id': '1198164443', 'pan': 9.89, 'tilt': -6.84, 'zoom': 0}},
    {'name': '대운', 'addr': '경기 김포시', 'pov': {'id': '1203824302', 'pan': 182.43, 'tilt': -2.92, 'zoom': 0}}
]

# 4. Apply Updates
updated_count = 0
for update in updates:
    for shop in data:
        name_ok = update['name'] in shop['n']
        addr_match = update['addr'] in shop['a']
        
        # Special check for generic names
        if update['name'] in ['가로판매소', '버스매표소', '신문가판점']:
            # Address must match more strictly if possible, or assume combination is unique
            pass

        if name_ok and addr_match:
            print(f"Updating: {shop['n']} ({shop['a']})")
            shop['pov'] = {
                "id": str(update['pov']['id']),
                "pan": float(update['pov']['pan']),
                "tilt": float(update['pov']['tilt']),
                "zoom": int(update['pov']['zoom'])
            }
            updated_count += 1

# 5. Save
with open(src_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Updated {updated_count} records.")
