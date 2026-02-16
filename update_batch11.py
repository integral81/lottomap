import json
import os
import shutil
from datetime import datetime

# 1. Backup
src_file = 'lotto_data.json'
backup_file = f'lotto_data_backup_batch11_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
shutil.copy(src_file, backup_file)
print(f"Backup created: {backup_file}")

# 2. Load Data
with open(src_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 3. Define Updates
updates = [
    {
        'name': '가판점(신문)',
        'addr': '서울 영등포구',
        'pov': {'id': '1198369749', 'pan': 11.08, 'tilt': -3.93, 'zoom': 0}
    },
    {
        'name': '마두역상행선 가판대',
        'addr': '경기 고양시',
        'pov': {'id': '1203613602', 'pan': 236.18, 'tilt': -1.45, 'zoom': 1}
    },
    {
        'name': 'GS25', # Name in DB might be GS25(Something)
        'addr': '경남 양산시', # Pyeongsan-dong
        'sub_mark': '양산문성',
        'pov': {'id': '1204592950', 'pan': 263.70, 'tilt': -9.48, 'zoom': 1}
    },
    {
        'name': '베스토아', # Name might be Bestoa(Yongjeon 2-ho)
        'addr': '대전 동구',
        'sub_mark': '용전',
        'pov': {'id': '1201601967', 'pan': 252.21, 'tilt': -7.83, 'zoom': 0}
    }
]

# 4. Apply Updates
updated_count = 0
for update in updates:
    for shop in data:
        # Check Name
        name_ok = update['name'] in shop['n']
        
        # Check Addr
        addr_ok = update['addr'] in shop['a']
        
        # Check Sub Mark (if needed)
        sub_ok = True
        if 'sub_mark' in update:
            sub_ok = update['sub_mark'] in shop['n'] or update['sub_mark'] in shop['a'] or (update['name'] == 'GS25' and 'GS25' in shop['n'])
            # For GS25 matching, address is strong filter.
            
        if name_ok and addr_ok:
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
