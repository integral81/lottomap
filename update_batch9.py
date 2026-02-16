import json
import os
import shutil
from datetime import datetime

# 1. Backup
src_file = 'lotto_data.json'
backup_file = f'lotto_data_backup_batch9_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
shutil.copy(src_file, backup_file)
print(f"Backup created: {backup_file}")

# 2. Load Data
with open(src_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Loaded {len(data)} records.")

# 3. Define Updates
updates = [
    {
        'name': '노다지복권방',
        'addr': '인천 미추홀구', # User said Han-naru-ro
        'sub_addr': '한나루로',
        'pov': {'id': '1199931642', 'pan': 124.91, 'tilt': 5.42, 'zoom': -2}
    },
    {
        'name': '노다지복권방',
        'addr': '대전 대덕구', # Shintanjin-ro
        'sub_addr': '신탄진로',
        'pov': {'id': '1201135496', 'pan': 257.55, 'tilt': -1.48, 'zoom': -2}
    },
    {
        'name': '노다지복권방',
        'addr': '인천', # User said Nam-gu Hakik-dong. Might be Michuhol-gu in data or Nam-gu.
        'sub_addr': '학익동',
        'pov': {'id': '1172510553', 'pan': 52.47, 'tilt': -1.06, 'zoom': -2}
    },
    {
        'name': '노다지복권방',
        'addr': '서울 종로구', # Changsin-dong
        'sub_addr': '창신동',
        'pov': {'id': '1197814475', 'pan': 349.49, 'tilt': 2.46, 'zoom': -2}
    },
    {
        'name': '노다지복권방',
        'addr': '충남 천안시', # Dongnam-gu
        'sub_addr': '동남구',
        'pov': {'id': '1194799836', 'pan': 331.31, 'tilt': 1.51, 'zoom': -3}
    },
    {
        'name': '노다지복권방',
        'addr': '대전 동구', # Seongnam-dong
        'sub_addr': '성남동',
        'pov': {'id': '1201115927', 'pan': 240.46, 'tilt': -1.08, 'zoom': 0}
    }
]

# 4. Apply Updates
updated_count = 0
not_found = []

for update in updates:
    found = False
    for shop in data:
        shop_name = shop.get('n', '').replace(' ', '')
        update_name_clean = update['name'].replace(' ', '')
        shop_addr = shop.get('a', '')
        
        # Name match
        if update_name_clean not in shop_name:
            continue
            
        # Address match
        # Try matching the main addr part
        if update['addr'] not in shop_addr:
            # Handle Incheon Nam-gu vs Michuhol-gu special case
            if update['addr'] == '인천' and ('남구' in shop_addr or '미추홀구' in shop_addr):
                pass # Continue to sub_addr check
            else:
                continue
                
        # Sub address match (critical for distinguishing same-name shops)
        if 'sub_addr' in update and update['sub_addr'] not in shop_addr:
            continue
            
        print(f"Updating: {shop['n']} ({shop['a']})")
        shop['pov'] = {
            "id": str(update['pov']['id']),
            "pan": float(update['pov']['pan']),
            "tilt": float(update['pov']['tilt']),
            "zoom": int(update['pov']['zoom'])
        }
        updated_count += 1
        found = True
        
    if not found:
        not_found.append(f"{update['name']} ({update.get('addr','')} {update.get('sub_addr','')})")

# 5. Save
with open(src_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Updated {updated_count} records.")
if not_found:
    print("WARNING: The following shops were not found:")
    for nf in not_found:
        print(f"- {nf}")
