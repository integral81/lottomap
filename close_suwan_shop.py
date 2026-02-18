import json
import os

f_json = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json'
f_js = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js'

with open(f_json, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Target: 세븐일레븐 수완점 (Gwangju Gwangsan-gu Suwan-dong 1428)
target_addr_part = "수완동 1428"
target_name_part = "세븐일레븐"

updated_count = 0
for s in data:
    addr = s.get('a', '')
    name = s.get('n', '')
    if target_addr_part in addr and target_name_part in name:
        s['closed'] = True
        updated_count += 1

if updated_count > 0:
    with open(f_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    with open(f_js, 'w', encoding='utf-8') as f:
        f.write('const lottoData = ' + json.dumps(data, ensure_ascii=False) + ';')
    
    print(f"Marked {updated_count} records for '세븐일레븐 수완점' as CLOSED.")
else:
    print("No matches found to close.")
