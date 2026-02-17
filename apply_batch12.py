import json
import os

f_json = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json'
f_js = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js'

with open(f_json, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Batch 12 Data
batch12 = [
    # New Registrations
    { "name": "CU노서점", "addr": "경북 경주시 금성로259번길 38 1층 CU 노서점 내", "panoid": 1187221443, "pov": { "pan": 45.67, "tilt": 3.22, "zoom": -1 } },
    { "name": "로또복권 황성점", "addr": "경북 경주시 황성동 472-8", "panoid": 1187151971, "pov": { "pan": 316.37, "tilt": 6.20, "zoom": -3 } },
    { "name": "영화유통", "addr": "경북 포항시 북구 양학천로 15", "panoid": 1187457532, "pov": { "pan": 30.96, "tilt": -3.64, "zoom": 1 } },
    # Updates (Refined)
    { "name": "해피복권방", "addr": "경기 고양시 일산동구 성석동 1246-80", "panoid": 1203594365, "pov": { "pan": 98.22, "tilt": 3.97, "zoom": 2 } },
    { "name": "알뜰슈퍼", "addr": "경기 동두천시 평화로 2436-1", "panoid": 1192812778, "pov": { "pan": 99.76, "tilt": 2.31, "zoom": 2 } },
    { "name": "다음정보텔레콤", "addr": "경남 진주시 평거동 200-1", "panoid": 1192979349, "pov": { "pan": 224.21, "tilt": 0.11, "zoom": 2 } }
]

updated_count = 0
for s in data:
    for b in batch12:
        # Match by name part
        if b['name'] in s.get('n', ''):
            s['panoid'] = b['panoid']
            # Ensure POV has ID
            pov_data = b['pov'].copy()
            pov_data['id'] = b['panoid']
            s['pov'] = pov_data
            updated_count += 1

if updated_count > 0:
    with open(f_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    with open(f_js, 'w', encoding='utf-8') as f:
        f.write('const lottoData = ' + json.dumps(data, ensure_ascii=False) + ';')
    
    print(f"Updated {updated_count} records for Batch 12.")
else:
    print("No matches found for Batch 12.")
