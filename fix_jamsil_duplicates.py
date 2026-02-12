import json

# Read lotto_data.json
with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Standardized coordinates and address for 잠실매점
CORRECT_LAT = 37.5144273491608
CORRECT_LNG = 127.100611434725
CORRECT_ADDRESS = "서울 송파구 올림픽로 269 1층 잠실역 8번출구 앞"

# Find all entries with '잠실매점' and standardize them
jamsil_count = 0
updated_count = 0

for entry in data:
    if '잠실매점' in entry['n']:
        jamsil_count += 1
        # Update coordinates and address
        entry['lat'] = CORRECT_LAT
        entry['lng'] = CORRECT_LNG
        entry['a'] = CORRECT_ADDRESS
        updated_count += 1

print(f"Found {jamsil_count} entries with '잠실매점'")
print(f"Updated {updated_count} entries")

# Save back to file
with open('lotto_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n잠실매점 데이터 통합 완료!")
print(f"모든 잠실매점이 단일 좌표로 통합되었습니다:")
print(f"  위도: {CORRECT_LAT}")
print(f"  경도: {CORRECT_LNG}")
print(f"  주소: {CORRECT_ADDRESS}")
