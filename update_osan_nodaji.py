import json
import os
import shutil
from datetime import datetime

# 1. Backup
src_file = 'lotto_data.json'
backup_file = f'lotto_data_backup_osan_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
shutil.copy(src_file, backup_file)
print(f"Backup created: {backup_file}")

# 2. Load Data
with open(src_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 3. Find and Update
target_name = "노다지복권방"
old_addr_part = "오산동 394-1"
new_addr = "경기 오산시 오산로 298-1 (오산동 394-1)"
# Confirmed Road Address: Osan-ro 298-1
# Keeping format: "Province City Road (Dong)" or standard.
# Existing data often uses Dong address.
# Let's use the explicit Format: "경기 오산시 오산로 298-1 (오산동 394-1)" 
# to be super clear as per user request context.

updated = False
for shop in data:
    if shop['n'] == target_name and '오산' in shop['a'] and ('394' in shop['a'] or '371' in shop['a']):
        print(f"Found shop: {shop['n']} ({shop['a']})")
        shop['a'] = new_addr
        updated = True
        print(f"Updated to: {shop['a']}")
        
        # Clear POV to force re-registration
        if 'pov' in shop:
            print("Clearing existing POV to force re-registration.")
            del shop['pov']

if updated:
    with open(src_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Saved changes.")
else:
    print("Shop not found.")
