import json
import os
import shutil
from datetime import datetime

# 1. Backup
src_file = 'lotto_data.json'
backup_file = f'lotto_data_backup_batch13_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
shutil.copy(src_file, backup_file)
print(f"Backup created: {backup_file}")

# 2. Load Data
with open(src_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 3. Define Updates
updates = [
    {'name': '토큰판매소', 'addr': '서울 송파구', 'pov': {'id': '1198482657', 'pan': 286.64, 'tilt': 0.37, 'zoom': 2}},
    {'name': '대박복권방', 'addr': '경기 연천군', 'pov': {'id': '1175550133', 'pan': 273.69, 'tilt': 2.40, 'zoom': 0}},
    {'name': '셀프카메라', 'addr': '부산 부산진구', 'pov': {'id': '1202587961', 'pan': 127.89, 'tilt': 4.44, 'zoom': 0}},
    {'name': '대박로또판매점', 'addr': '경기 수원시', 'pov': {'id': '1199673044', 'pan': 254.32, 'tilt': 0.39, 'zoom': 0}},
    {'name': '지원물산', 'addr': '서울 노원구', 'pov': {'id': '1198350307', 'pan': 55.64, 'tilt': -4.99, 'zoom': -3}}
]

# 4. Apply Updates
updated_count = 0
for update in updates:
    for shop in data:
        name_ok = update['name'] in shop['n']
        addr_match = update['addr'] in shop['a']
        
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
