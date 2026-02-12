import json

# Read lotto_data.json
with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Correct coordinates from user's Kakao Map link
CORRECT_LAT = 37.66146073470035
CORRECT_LNG = 127.05799532551201
CORRECT_ADDRESS = "서울 노원구 동일로 1493 상계주공아파트(10단지) 주공10단지종합상가111"

# Update all '스파' entries
updated_count = 0
for entry in data:
    if entry['n'] == '스파':
        entry['lat'] = CORRECT_LAT
        entry['lng'] = CORRECT_LNG
        entry['a'] = CORRECT_ADDRESS
        updated_count += 1

print(f"Updated {updated_count} entries with name '스파'")

# Save back to file
with open('lotto_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n스파 데이터 통합 완료!")
print(f"  위도: {CORRECT_LAT}")
print(f"  경도: {CORRECT_LNG}")
print(f"  주소: {CORRECT_ADDRESS}")
