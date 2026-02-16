import json
import os
import shutil
from datetime import datetime

# 1. Backup
src_file = 'lotto_data.json'
backup_file = f'lotto_data_backup_paju_final_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
shutil.copy(src_file, backup_file)
print(f"Backup created: {backup_file}")

# 2. Load Data
with open(src_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 3. Apply Update
target_name = "노다지복권방"
target_pov = {'id': '1203066558', 'pan': 244.34, 'tilt': -3.68, 'zoom': -3}
target_addr_hint = "파주시 문산읍"

updated = False
for shop in data:
    # Match criteria
    is_nodaji = '노다지' in shop['n']
    is_paju = '파주' in shop['a'] and '문산' in shop['a']
    
    if is_nodaji and is_paju:
        print(f"Found shop: {shop['n']} ({shop['a']})")
        
        # 1. Clean Name (Remove ★ if present)
        shop['n'] = "노다지복권방" 
        
        # 2. Update Address (Standardize to what we found or keep as is if robust)
        # User accepted 6-28 or found it there? 
        # Actually user found POV at 1203066558. Let's use the address associated with the shop in our DB
        # or update to the one user likely found.
        # Let's keep the address we corrected to earlier or the one that works.
        # Current DB state might be "문산리 6-28" from previous step, or user cancelled the revert?
        # Let's check current value.
        
        # 3. Update POV
        shop['pov'] = {
            "id": str(target_pov['id']),
            "pan": float(target_pov['pan']),
            "tilt": float(target_pov['tilt']),
            "zoom": int(target_pov['zoom'])
        }
        updated = True
        print("Updated Name, Address(kept), and POV.")

if updated:
    with open(src_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Saved changes.")
else:
    print("Shop not found.")
