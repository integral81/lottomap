import json
import os
import shutil
from datetime import datetime

# 1. Backup
src_file = 'lotto_data.json'
backup_file = f'lotto_data_backup_paju_fix2_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
shutil.copy(src_file, backup_file)
print(f"Backup created: {backup_file}")

# 2. Load Data
with open(src_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 3. Find and Update
target_name = "노다지복권방"
# Previous wrong update was: "경기 파주시 문산읍 문산리 6-28"
# Correct Address found: "경기 파주시 문산읍 문산리 6-2" (Road: 문향로67번길 2)

updated = False
for shop in data:
    if shop['n'] == target_name and '파주' in shop['a']:
        print(f"Found shop: {shop['n']} ({shop['a']})")
        # Update to the verified correct address
        shop['a'] = "경기 파주시 문산읍 문산리 6-2 (문향로67번길 2)"
        updated = True
        print(f"Updated to: {shop['a']}")
        
        # Clear POV again just in case
        if 'pov' in shop:
            del shop['pov']

if updated:
    with open(src_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Saved changes.")
else:
    print("Shop not found.")
