import json
import os
import shutil
from datetime import datetime

# 1. Backup
src_file = 'lotto_data.json'
backup_file = f'lotto_data_backup_sky_lotto_close_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
shutil.copy(src_file, backup_file)
print(f"Backup created: {backup_file}")

# 2. Load Data
with open(src_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 3. Mark Sky Lotto (Yeoju) as Closed/Hidden
target_name = "하늘로또"
target_addr_fragment = "세종로475번길 2" 

updated = False
for shop in data:
    if target_name in shop['n'] and target_addr_fragment in shop['a']:
        print(f"Found shop: {shop['n']} ({shop['a']})")
        
        # User Feedback: "Cannot find it on Roadview. Accuracy is key. Better to not show it."
        # Action: Mark as closed or add a special flag to hide or show warning.
        # Since we don't have a 'hidden' flag in the UI logic explicitly shown, 'isClosed' is the safest 'don't go there' signal.
        # Or we can keep it open but REMOVE the POV so it doesn't show a misleading view, 
        # AND add a 'customMessage' saying "Location Unverified / Signage Invisible".
        
        # However, user said: "폐점인 매장에 폐점으로 기재하지 않거나... 고객은 헛걸음을 하게되어..."
        # So marking it isClosed = True seems most aligned with "Safety/Accuracy first".
        
        shop['isClosed'] = True
        shop['customMessage'] = "로드뷰상 매장 간판 식별 불가 (방문 유의)"
        
        # Also clear POV just in case
        if 'pov' in shop:
            del shop['pov']
            
        print("  Marked as isClosed=True and added warning message.")
        updated = True

if updated:
    with open(src_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Saved changes.")
else:
    print("Shop not found in DB.")
