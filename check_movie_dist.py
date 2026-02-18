import json

f_json = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json'

with open(f_json, 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=== Addresses for 영화유통 variants ===")
matches = [s for s in data if '영화유통' in s.get('n', '')]
for m in matches:
    print(f"Name: {m.get('n')}")
    print(f"Addr: {m.get('a')}")
    print(f"Lat: {m.get('lat')}, Lng: {m.get('lng')}")
    print(f"POV: {bool(m.get('panoid'))}")
    print("-" * 20)
