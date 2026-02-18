import json
import os

f_json = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json'
f_js = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js'

with open(f_json, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Shop details provided by user
target_name = "옥좌로또점"
panoid = 1187799279
pov = {"id": 1187799279, "pan": 322.70, "tilt": 3.52, "zoom": 3}

updated_count = 0
for s in data:
    if target_name in s.get('n', ''):
        s['panoid'] = panoid
        s['pov'] = pov
        updated_count += 1

if updated_count > 0:
    with open(f_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    with open(f_js, 'w', encoding='utf-8') as f:
        f.write('const lottoData = ' + json.dumps(data, ensure_ascii=False) + ';')
    
    print(f"Updated {updated_count} records for {target_name}.")
else:
    print(f"{target_name} not found in database.")
