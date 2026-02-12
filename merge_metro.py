import json

# Read lotto_data.json
with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Define unified coordinates (from User's Google Maps link pinpoint)
UNI_LAT = 35.865918
UNI_LNG = 128.5960254

count = 0
for item in data:
    if '메트로센터점' in item['n']:
        item['lat'] = UNI_LAT
        item['lng'] = UNI_LNG
        count += 1

# Write back
with open('lotto_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'Successfully unified {count} entries for 메트로센터점 at {UNI_LAT}, {UNI_LNG}')
