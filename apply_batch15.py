import json
import os

f_json = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json'
f_js = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js'

with open(f_json, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Batch 15 Data
batch15 = [
    { "name": "타운복권방", "addr": "광주 북구 밤실로 184-1", "panoid": 1200747212, "pov": { "pan": 57.83, "tilt": -0.92, "zoom": -3 } },
    { "name": "세븐일레븐동천점", "addr": "광주 서구 동천동 600 세븐일레븐 동천점 내", "panoid": 1200054546, "pov": { "pan": 75.76, "tilt": -2.70, "zoom": 2 } },
    { "name": "천국열쇠", "addr": "광주 북구 운암동 1040-10", "panoid": 1200807885, "pov": { "pan": 225.62, "tilt": -0.26, "zoom": 0 } },
    { "name": "백송마트", "addr": "광주 광산구 월계로 110 104호", "panoid": 1200002434, "pov": { "pan": 197.60, "tilt": 4.41, "zoom": -1 } }
]

updated_count = 0
for s in data:
    for b in batch15:
        if b['name'] in s.get('n', ''):
            s['panoid'] = b['panoid']
            pov_data = b['pov'].copy()
            pov_data['id'] = b['panoid']
            s['pov'] = pov_data
            updated_count += 1

if updated_count > 0:
    with open(f_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    with open(f_js, 'w', encoding='utf-8') as f:
        f.write('const lottoData = ' + json.dumps(data, ensure_ascii=False) + ';')
    
    print(f"Updated {updated_count} records for Batch 15.")
else:
    print("No matches found for Batch 15.")
