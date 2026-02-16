import json
import os
import shutil
from datetime import datetime

# 1. Backup
src_file = 'lotto_data.json'
backup_file = f'lotto_data_backup_sky_lotto_restore_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
shutil.copy(src_file, backup_file)
print(f"Backup created: {backup_file}")

# 2. Load Data
with open(src_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 3. Restore Sky Lotto (Yeoju)
target_name = "하늘로또"
target_addr_fragment = "세종로475번길 2" 

updated = False
for shop in data:
    if target_name in shop['n'] and target_addr_fragment in shop['a']:
        print(f"Found shop: {shop['n']} ({shop['a']})")
        
        # Restore Status
        if 'isClosed' in shop:
            del shop['isClosed'] # Valid shop
        
        # Update custom message to be helpful but accurate
        shop['customMessage'] = "1197회 2등 당첨점 (로드뷰 미식별 매장 - 성도빌딩 확인 요망)"
        
        # Remove POV to prevent showing empty/wrong street view
        if 'pov' in shop:
            del shop['pov']
            
        print("  Restored shop status. Removed isClosed. Added helper message.")
        updated = True

if updated:
    with open(src_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Saved changes.")
else:
    print("Shop not found in DB.")
