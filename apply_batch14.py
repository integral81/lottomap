import json
import os

f_json = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json'
f_js = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js'

with open(f_json, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Batch 14 Data
target_name = "영화복권"
target_addr_part = "상무버들로" # Unique enough for this shop
# User POV
new_panoid = 1200303825
new_pov = { "id": 1200303825, "pan": 3.39, "tilt": 4.75, "zoom": 1 }

updated_count = 0
for s in data:
    if target_name in s.get('n', '') and target_addr_part in s.get('a', ''):
        s['panoid'] = new_panoid
        s['pov'] = new_pov
        updated_count += 1

if updated_count > 0:
    with open(f_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    with open(f_js, 'w', encoding='utf-8') as f:
        f.write('const lottoData = ' + json.dumps(data, ensure_ascii=False) + ';')
    
    print(f"Updated {updated_count} records for '영화복권(버들점)' (Batch 14).")
else:
    print("No matches found for '영화복권(버들점)'. Checking broader search...")
    # Fallback search if strict match fails
    for s in data:
        if "영화" in s.get('n', '') and "버들" in s.get('n', ''):
             print(f"Found potential match: {s.get('n')} / {s.get('a')}")

