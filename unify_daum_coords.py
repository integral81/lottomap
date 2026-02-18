import json

f_json = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json'
f_js = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js'

with open(f_json, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 1. Unify '다음정보텔레콤' coordinates
target_name = "다음정보텔레콤"
# Use the coordinates of the entry that has the 'pov' field (from Batch 12)
# We know from previous steps we updated all of them to have panoid, but let's pick the one with "CU" in address as the anchor if possible, or just the first one.
# Actually, the user updated '다음정보텔레콤' in Batch 12.
# Let's find the reference coordinates (likely the one matching Batch 12 address).
ref_lat = 35.173110601323
ref_lng = 128.061804222495

count = 0
for s in data:
    if target_name in s.get('n', ''):
        s['lat'] = ref_lat
        s['lng'] = ref_lng
        count += 1

print(f"Unified {count} records for {target_name}.")

# 2. Check '영화유통'
print("\n--- Checking 영화유통 (Movie Distribution) ---")
movie_shops = [s for s in data if "영화유통" in s.get('n', '')]
for s in movie_shops:
    print(f"Name: {s.get('n')}, Addr: {s.get('a')}, Lat: {s.get('lat')}")

with open(f_json, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

with open(f_js, 'w', encoding='utf-8') as f:
    f.write('const lottoData = ' + json.dumps(data, ensure_ascii=False) + ';')
