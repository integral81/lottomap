import json

# Read lotto_data.json
with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# New accurate coordinates from user's Roughmap
CORRECT_LAT = 37.51403647814415
CORRECT_LNG = 127.10115723494299
CORRECT_ADDRESS = "서울 송파구 올림픽로 269 1층 잠실역 8번출구 앞"

# Update all 잠실매점 entries
updated_count = 0
for entry in data:
    if '잠실매점' in entry['n']:
        entry['lat'] = CORRECT_LAT
        entry['lng'] = CORRECT_LNG
        entry['a'] = CORRECT_ADDRESS
        updated_count += 1

print(f"Updated {updated_count} entries with new coordinates")

# Save back to file
with open('lotto_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n✅ 잠실매점 좌표 업데이트 완료!")
print(f"  위도: {CORRECT_LAT}")
print(f"  경도: {CORRECT_LNG}")
print(f"  주소: {CORRECT_ADDRESS}")
