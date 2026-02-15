import json

# Read lotto_data.json
with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Current address info for World Cup Lottery
CURRENT_LAT = 37.4099289865478
CURRENT_LNG = 127.258382575225
CURRENT_ADDRESS = "경기 광주시 경안로 20 (경안동)"

# Find all '월드컵복권방' entries and standardize them
updated_count = 0
for entry in data:
    if '월드컵' in entry['n'] and '복권방' in entry['n']:
        # Update coordinates and address to the current location
        entry['lat'] = CURRENT_LAT
        entry['lng'] = CURRENT_LNG
        entry['a'] = CURRENT_ADDRESS
        updated_count += 1

print(f"Updated {updated_count} entries for '월드컵복권방'")

# Save back to file
with open('lotto_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n월드컵복권방 데이터 통합 완료!")
print(f"  위도: {CURRENT_LAT}")
print(f"  경도: {CURRENT_LNG}")
print(f"  주소: {CURRENT_ADDRESS}")
