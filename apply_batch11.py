import json
import os

f_json = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json'
f_js = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js'

with open(f_json, 'r', encoding='utf-8') as f:
    data = json.load(f)

batch11 = [
    { "name": "해피복권방", "addr": "경기 고양시 일산동구 성석동 1246-80", "panoid": 1203594365, "pov": { "pan": 93.22, "tilt": 4.78, "zoom": 2 } },
    { "name": "알뜰슈퍼", "addr": "경기 동두천시 평화로 2436-1 4/6", "panoid": 1192812778, "pov": { "pan": 83.08, "tilt": 7.25, "zoom": 3 } },
    { "name": "다음정보텔레콤", "addr": "경남 진주시 평거동 200-1 CU편의점 내", "panoid": 1192980927, "pov": { "pan": 208.90, "tilt": 4.53, "zoom": 0 } },
    { "name": "공단로또점", "addr": "경남 함안군 삼칠로 831 슈퍼 옆", "panoid": 1191986142, "pov": { "pan": 227.22, "tilt": 2.08, "zoom": 3 } }
]

updated_count = 0
for s in data:
    for b in batch11:
        # Match by name part to ensure we catch variations like "다음정보텔레콤(훼미리마트내)"
        if b['name'] in s.get('n', ''):
            s['panoid'] = b['panoid']
            # Ensure POV has ID for consistency
            pov_data = b['pov'].copy()
            pov_data['id'] = b['panoid']
            s['pov'] = pov_data
            updated_count += 1

if updated_count > 0:
    with open(f_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    with open(f_js, 'w', encoding='utf-8') as f:
        f.write('const lottoData = ' + json.dumps(data, ensure_ascii=False) + ';')
    
    print(f"Updated {updated_count} records for Batch 11.")
else:
    print("No matches found for Batch 11.")
