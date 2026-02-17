import json
import os

f_json = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json'
f_js = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js'

with open(f_json, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 1. Batch 13 Registration
batch13 = [
    { "name": "대야지복권", "addr": "광주 남구 주월동 961-24번지", "panoid": 1200569355, "pov": { "pan": 341.43, "tilt": 4.40, "zoom": -1 } },
    { "name": "동원슈퍼", "addr": "광주 남구 월산5동 1053-22", "panoid": 1200403334, "pov": { "pan": 234.03, "tilt": -0.89, "zoom": -1 } },
    { "name": "빛고을로또", "addr": "광주 광산구 소촌로 147 세븐일레븐", "panoid": 1200047805, "pov": { "pan": 251.34, "tilt": -0.94, "zoom": -1 } },
    { "name": "1등로또방", "addr": "광주 동구 중앙로 249-2", "panoid": 1200326817, "pov": { "pan": 313.12, "tilt": 6.55, "zoom": -1 } }
]

count_b13 = 0
for s in data:
    for b in batch13:
        if b['name'] in s.get('n', ''):
            s['panoid'] = b['panoid']
            pov_data = b['pov'].copy()
            pov_data['id'] = b['panoid']
            s['pov'] = pov_data
            count_b13 += 1

print(f"Registered {count_b13} records for Batch 13.")

# 2. Consolidation: 영화유통 (Ulsan -> Pohang)
target_movie = "영화유통"
src_part = "울산"
dst_addr = "경북 포항시 북구 양학천로 15"
dst_lat = 36.0237320718825
dst_lng = 129.353914672823
dst_panoid = 1187457532
dst_pov = { "id": 1187457532, "pan": 30.96, "tilt": -3.64, "zoom": 1 }

count_movie = 0
for s in data:
    if target_movie in s.get('n', '') and src_part in s.get('a', ''):
        s['a'] = dst_addr
        s['lat'] = dst_lat
        s['lng'] = dst_lng
        s['panoid'] = dst_panoid
        s['pov'] = dst_pov.copy()
        count_movie += 1

print(f"Merged {count_movie} '영화유통' records to Pohang.")

# 3. Consolidation: 다음정보텔레콤 (Unify Coords)
target_daum = "다음정보텔레콤"
ref_lat = 35.173110601323
ref_lng = 128.061804222495

count_daum = 0
for s in data:
    if target_daum in s.get('n', ''):
        s['lat'] = ref_lat
        s['lng'] = ref_lng
        count_daum += 1

print(f"Unified coords for {count_daum} '다음정보텔레콤' records.")

# Save
with open(f_json, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

with open(f_js, 'w', encoding='utf-8') as f:
    f.write('const lottoData = ' + json.dumps(data, ensure_ascii=False) + ';')
