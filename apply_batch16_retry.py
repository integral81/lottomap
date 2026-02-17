import json
import os

f_json = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json'
f_js = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js'

with open(f_json, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Batch 16 Data (Fixed & Updated)
batch16 = [
    { "name": "베스트원", "addr": "전남 영광군 영광읍 남천리 315 CU편의점", "panoid": 1192687174, "pov": { "pan": 329.07, "tilt": -1.13, "zoom": -1 } },
    { "name": "춘향로또", "addr": "전북 남원시 동림로 102-1", "panoid": 1205554323, "pov": { "pan": 43.12, "tilt": 4.30, "zoom": -1 } },
    { "name": "복권판매소", "addr": "대구 서구 국채보상로 438", "panoid": 1201562075, "pov": { "pan": 211.45, "tilt": -3.22, "zoom": -3 } },
    { "name": "청구마트", "addr": "대구 북구 검단로 34 청구아파트상가108동102호", "panoid": 1034649551, "pov": { "pan": 68.72, "tilt": -0.84, "zoom": -3 } },
    { "name": "월드복권", "addr": "대구 서구 북비산로 98", "panoid": 1201401917, "pov": { "pan": 182.02, "tilt": 1.13, "zoom": -2 } },
    { "name": "대흥당", "addr": "전북 정읍시 관통로 102", "panoid": 1183542559, "pov": { "pan": 331.55, "tilt": -2.95, "zoom": 1 } },
    { "name": "광포로또복권", "addr": "경북 울진군 죽변북로 154", "panoid": 1186537308, "pov": { "pan": 76.85, "tilt": 1.39, "zoom": 2 } },
    { "name": "로또복권애니타임점", "addr": "경북 구미시 인동중앙로11길 24 애니타임편의점 내", "panoid": 1166104869, "pov": { "pan": 358.26, "tilt": 8.89, "zoom": -1 } },
    { "name": "스타마트", "addr": "경북 구미시 임은길 15", "panoid": 1165804529, "pov": { "pan": 315.05, "tilt": 4.10, "zoom": -1 } },
    { "name": "로또복권4공단점", "addr": "경북 구미시 첨단기업1로 18", "panoid": 1166471935, "pov": { "pan": 125.32, "tilt": 8.74, "zoom": -1 } },
    { "name": "GMART", "addr": "경북 구미시 구미중앙로 57-3", "panoid": 1165801425, "pov": { "pan": 23.31, "tilt": -1.02, "zoom": 0 } },
    { "name": "로또로복권", "addr": "전북 전주시 완산구 모악로 4729", "panoid": 1172287937, "pov": { "pan": 304.48, "tilt": 1.34, "zoom": 0 } }
]

updated_count = 0
for s in data:
    for b in batch16:
        if b['name'] in s.get('n', ''):
             # Ensure correct matching for "복권판매소" which is generic
            if b['name'] == "복권판매소" and "국채보상로" not in s.get('a', ''):
                continue
                
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
    
    print(f"Updated {updated_count} records for Batch 16.")
else:
    print("No matches found for Batch 16.")
