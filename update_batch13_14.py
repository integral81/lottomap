import json
import os
import shutil
from datetime import datetime

# 1. Backup
src_file = 'lotto_data.json'
backup_file = f'lotto_data_backup_batch13_14_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
shutil.copy(src_file, backup_file)
print(f"Backup created: {backup_file}")

# 2. Load Data
with open(src_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 3. Define Updates (Batch 13 + 14)
updates = [
    # Batch 13 (Missed)
    {'name': '토큰판매소', 'addr': '서울 송파구', 'pov': {'id': '1198482657', 'pan': 286.64, 'tilt': 0.37, 'zoom': 2}},
    {'name': '대박복권방', 'addr': '경기 연천군', 'pov': {'id': '1175550133', 'pan': 273.69, 'tilt': 2.40, 'zoom': 0}},
    {'name': '셀프카메라', 'addr': '부산 부산진구', 'pov': {'id': '1202587961', 'pan': 127.89, 'tilt': 4.44, 'zoom': 0}},
    {'name': '대박로또판매점', 'addr': '경기 수원시', 'pov': {'id': '1199673044', 'pan': 254.32, 'tilt': 0.39, 'zoom': 0}},
    {'name': '지원물산', 'addr': '서울 노원구', 'pov': {'id': '1198350307', 'pan': 55.64, 'tilt': -4.99, 'zoom': -3}},
    
    # Batch 14 (New)
    {'name': '로또명당가두판매점', 'addr': '경기 안양시', 'pov': {'id': '1203179429', 'pan': 21.42, 'tilt': -1.47, 'zoom': -2}},
    {'name': '소리창고', 'addr': '서울 강서구', 'pov': {'id': '1198604052', 'pan': 110.49, 'tilt': -1.94, 'zoom': -1}},
    {'name': '가판점', 'addr': '경기 부천시', 'pov': {'id': '1203727505', 'pan': 50.11, 'tilt': 1.33, 'zoom': 3}},
    {'name': '나나 복권판매소', 'addr': '경남 양산시', 'pov': {'id': '1204563526', 'pan': 267.03, 'tilt': 5.70, 'zoom': 1}}, # Name spacing check needed
    {'name': '기장슈퍼', 'addr': '부산 기장군', 'pov': {'id': '1033564888', 'pan': 353.15, 'tilt': 3.46, 'zoom': -1}},
    {'name': '대전우표사', 'addr': '대전 동구', 'pov': {'id': '1163576030', 'pan': 46.37, 'tilt': -3.01, 'zoom': -1}},
    {'name': '율암25시편의점', 'addr': '경기 화성시', 'pov': {'id': '1198087970', 'pan': 163.07, 'tilt': -1.49, 'zoom': 1}},
    {'name': '운좋은날', 'addr': '서울 강동구', 'pov': {'id': '1198599077', 'pan': 36.55, 'tilt': -0.28, 'zoom': 1}}
]

# 4. Apply Updates
updated_count = 0
for update in updates:
    for shop in data:
        # Normalize names for comparison (remove spaces)
        shop_name_clean = shop['n'].replace(" ", "")
        update_name_clean = update['name'].replace(" ", "")
        
        name_ok = update_name_clean in shop_name_clean or shop_name_clean in update_name_clean
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
            # Special fix for 'Nan' if needed, but the loop continues to find potential dupes? 
            # Usually strict match. Break if unique? No, lotto_data might have slight dupes, better update all matches.

# 5. Save
with open(src_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Updated {updated_count} records.")
