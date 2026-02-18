import json

f_json = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json'
f_js = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js'

with open(f_json, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Target: 영화유통 (Movie Distribution)
target_name = "영화유통"
# Source (Ulsan) criteria
src_part = "울산"
# Dest (Pohang) data
dst_addr = "경북 포항시 북구 양학천로 15"
dst_lat = 36.0237320718825
dst_lng = 129.353914672823
dst_panoid = 1187457532
dst_pov = { "id": 1187457532, "pan": 30.96, "tilt": -3.64, "zoom": 1 }

updated_count = 0
for s in data:
    if target_name in s.get('n', ''):
        # If it's the Ulsan entry, move it to Pohang
        if src_part in s.get('a', ''):
            s['a'] = dst_addr
            s['lat'] = dst_lat
            s['lng'] = dst_lng
            s['panoid'] = dst_panoid
            s['pov'] = dst_pov
            updated_count += 1

print(f"Moved {updated_count} '영화유통' records from Ulsan to Pohang.")

with open(f_json, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

with open(f_js, 'w', encoding='utf-8') as f:
    f.write('const lottoData = ' + json.dumps(data, ensure_ascii=False) + ';')
