import json
import os
import shutil
from datetime import datetime

# 1. Backup
src_file = 'lotto_data.json'
backup_file = f'lotto_data_backup_paju_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
shutil.copy(src_file, backup_file)
print(f"Backup created: {backup_file}")

# 2. Load Data
with open(src_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 3. Find and Update
target_name = "노다지복권방"
old_addr_part = "문산리 6-2"
new_addr = "경기 파주시 문산읍 문산로 44 (문산리 6-28)"
# Note: User mentioned 6-28. Road address is 'Munsan-ro 44'.
# Let's keep the format consistent with other data. 
# Usually we use Road Address if available, but for now let's stick to what user verified or standard format.
# The user specifically asked if 6-28 is correct.
# Updated Addr: "경기 파주시 문산읍 문산리 6-28" (cleaner for now, or mix)

updated = False
for shop in data:
    if shop['n'] == target_name and '파주' in shop['a'] and '문산' in shop['a']:
        print(f"Found shop: {shop['n']} ({shop['a']})")
        shop['a'] = "경기 파주시 문산읍 문산리 6-28" 
        # We can store the road address in a separate field if we had one, but 'a' is main identifier.
        updated = True
        print(f"Updated to: {shop['a']}")
        
        # Also clean up coords if they were based on 6-2?
        # The distance is very small, so existing coords might be 'okay' but specific POV needs to be re-checked.
        # User implies POV might be wrong because of address.
        # We will clear POV if it exists to force re-verification? 
        # Or just keep it and let user re-register?
        # User said "different place?" -> imply POV needs update.
        # Let's clear POV to be safe, so it appears in admin list again.
        if 'pov' in shop:
            print("Clearing existing POV to force re-registration.")
            del shop['pov']

if updated:
    with open(src_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Saved changes.")
else:
    print("Shop not found.")
