import json
import os
import shutil
from datetime import datetime

# 1. Backup
src_file = 'lotto_data.json'
backup_file = f'lotto_data_backup_batch15_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
shutil.copy(src_file, backup_file)
print(f"Backup created: {backup_file}")

# 2. Load Data
with open(src_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 3. Define Updates
updates = [
    {'name': '나눔로또봉평점', 'addr': '경남 통영시', 'pov': {'id': '1204285725', 'pan': 28.81, 'tilt': 0.62, 'zoom': 1}}
]

# 4. Apply Updates
updated_count = 0
for update in updates:
    for shop in data:
        # Check Name (handle spacing issues if any, but this seems clean)
        name_match = update['name'] in shop['n']
        addr_match = update['addr'] in shop['a']
        
        if name_match and addr_match:
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
