import json

# Read lotto_data.json
with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Correct values
NEW_ADDR = "부산 서구 자갈치로 4-1 1층"
NEW_LAT = 35.0961942484519
NEW_LNG = 129.024881334607

count = 0
for item in data:
    if '로터리복권방' in item['n'] and '부산' in item['a']:
        item['a'] = NEW_ADDR
        item['lat'] = NEW_LAT
        item['lng'] = NEW_LNG
        count += 1

# Write back
with open('lotto_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'Successfully updated {count} entries for 로터리복권방 with new address and coordinates.')
