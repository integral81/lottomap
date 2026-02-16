import json
import os
import shutil
from datetime import datetime

# 1. Backup
src_file = 'lotto_data.json'
backup_file = f'lotto_data_backup_batch10_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
shutil.copy(src_file, backup_file)
print(f"Backup created: {backup_file}")

# 2. Load Data
with open(src_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 3. Define Updates
updates = [
    {
        'name': '노다지복권방',
        'addr': '경기 오산시',
        'pov': {'id': '1174611564', 'pan': 158.12, 'tilt': -3.94, 'zoom': -1}
    },
    {
        'name': '황실복권방',
        'addr': '충남 천안시',
        'pov': {'id': '1193993670', 'pan': 325.61, 'tilt': 1.97, 'zoom': 2}
    },
    {
        'name': '북문복권방',
        'addr': '경기 수원시',
        'pov': {'id': '1199499154', 'pan': 255.46, 'tilt': -1.74, 'zoom': 2}
    }
]

# 4. Apply Updates
updated_count = 0
for update in updates:
    for shop in data:
        # Match Logic
        name_match = update['name'] in shop['n']
        # Special handling for Osan Nodaji to cleanup any potential ★ stars or ensure correct match
        if update['name'] == '노다지복권방' and '노다지' in shop['n']:
            name_match = True
        
        addr_match = update['addr'] in shop['a']
        
        if name_match and addr_match:
            print(f"Updating: {shop['n']} ({shop['a']})")
            
            # Clean name for Nodaji just in case
            if '노다지' in shop['n']:
                shop['n'] = "노다지복권방"
                
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
