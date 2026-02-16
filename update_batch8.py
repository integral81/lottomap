import json
import os
import shutil
from datetime import datetime

# 1. Backup
src_file = 'lotto_data.json'
backup_file = f'lotto_data_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
shutil.copy(src_file, backup_file)
print(f"Backup created: {backup_file}")

# 2. Load Data
with open(src_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Loaded {len(data)} records.")

# 3. Define Updates
updates = [
    {
        'name': '데이앤나잇',
        'addr': '서울 성북구',
        'pov': {'id': '1198236388', 'pan': 56.55, 'tilt': -0.44, 'zoom': 0}
    },
    {
        'name': '이마트24',
        'addr': '전남 순천시',
        'sub_mark': '순천산단점', # Optional helper for verifying
        'pov': {'id': '1205488417', 'pan': 289.33, 'tilt': -1.50, 'zoom': 2}
    },
    {
        'name': '25시슈퍼',
        'addr': '경기 시흥시',
        'pov': {'id': '1176030807', 'pan': 289.52, 'tilt': -3.30, 'zoom': 2}
    },
    {
        'name': '대성기획',
        'addr': '경기 용인시',
        'pov': {'id': '1199504553', 'pan': 2.77, 'tilt': -5.50, 'zoom': 1}
    },
    {
        'name': '중앙로또',
        'addr': '경북 칠곡군',
        'pov': {'id': '1167165616', 'pan': 281.02, 'tilt': -2.02, 'zoom': 1}
    },
    {
        'name': '노다지복권방',
        'addr': '경기 시흥시',
        'pov': {'id': '1175484804', 'pan': 297.64, 'tilt': 4.55, 'zoom': 1}
    },
    {
        'name': '노다지복권방',
        'addr': '부산 북구',
        'pov': {'id': '1202241625', 'pan': 136.18, 'tilt': 0.65, 'zoom': 1}
    }
]

# 4. Apply Updates
updated_count = 0
not_found = []

for update in updates:
    found = False
    for shop in data:
        # Normalize for comparison
        shop_name = shop.get('n', '').replace(' ', '')
        update_name_clean = update['name'].replace(' ', '')
        
        shop_addr = shop.get('a', '')
        
        # Check Name match (partial allowed if significant) or exact
        name_match = update_name_clean in shop_name
        
        # Check Address match
        addr_match = update['addr'] in shop_addr
        
        if name_match and addr_match:
            # Special check for multiple same-name shops (Nodaji)
            # The address filter usually handles it, but let's be safe
            print(f"Updating: {shop['n']} ({shop['a']})")
            
            # Construct POV object
            shop['pov'] = {
                "id": str(update['pov']['id']),
                "pan": float(update['pov']['pan']),
                "tilt": float(update['pov']['tilt']),
                "zoom": int(update['pov']['zoom'])
            }
            
            # Force coordinates update if needed? 
            # Usually coordinates are already correct if we found the shop.
            # But sometimes we might want to sync invalid coords?
            # For now, just update POV.
            
            updated_count += 1
            found = True
            # Don't break here if we want to update all history? 
            # Usually we update all duplicates.
            # But let's verify if there are duplicates.
            
    if not found:
        not_found.append(f"{update['name']} ({update['addr']})")

# 5. Save
with open(src_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Updated {updated_count} records.")
if not_found:
    print("WARNING: The following shops were not found:")
    for nf in not_found:
        print(f"- {nf}")
