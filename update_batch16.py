import json
import os
import shutil
from datetime import datetime

# 1. Backup
src_file = 'lotto_data.json'
backup_file = f'lotto_data_backup_batch16_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
shutil.copy(src_file, backup_file)
print(f"Backup created: {backup_file}")

# 2. Load Data
with open(src_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 3. Define Updates (Batch 16)
updates = [
    {'name': '광성슈퍼', 'addr': '경기 이천시', 'pov': {'id': '1175073795', 'pan': 287.83, 'tilt': -3.32, 'zoom': -3}},
    {'name': '장미슈퍼', 'addr': '충남 부여군', 'pov': {'id': '1178842351', 'pan': 262.74, 'tilt': -0.84, 'zoom': -3}},
    {'name': '까치복권방', 'addr': '경기 시흥시', 'pov': {'id': '1176040887', 'pan': 251.50, 'tilt': -3.98, 'zoom': -3}},
    {'name': '로또복권', 'addr': '경기 평택시', 'pov': {'id': '1197645356', 'pan': 242.27, 'tilt': -2.67, 'zoom': -3}}
]

# 4. Yeoju Sky Lotto Restoration (Confirm Active but Hidden from Admin)
sky_lotto_addr = "세종로475번길 2"
sky_lotto_name = "하늘로또"

# 5. Apply
updated_count = 0

# Apply Batch 16
for update in updates:
    for shop in data:
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

# Restore Sky Lotto (Verify it's NOT closed, but add message)
for shop in data:
    if sky_lotto_name in shop['n'] and sky_lotto_addr in shop['a']:
        print(f"Restoring Sky Lotto: {shop['n']}")
        # Remove isClosed if I added it previously (previous run was cancelled but better safe)
        if 'isClosed' in shop:
            del shop['isClosed']
        
        # Add custom message
        shop['customMessage'] = "1197회 2등 당첨점 (로드뷰 미식별 매장 - 성도빌딩 확인 요망)"
        
        # Ensure POV is empty so it doesn't show wrong view, BUT user wants it off admin list.
        # We will handle the "off admin list" part in generate_admin_list_final.py by using a filter.
        # Here we just ensure data is correct (Active, Message).
        if 'pov' in shop:
            del shop['pov'] # Clear it so it doesn't show wrong view
        
        updated_count += 1

# 6. Save
with open(src_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Updated {updated_count} records (Batch 16 + Sky Lotto).")
