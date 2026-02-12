import json

with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# The correct address from user image: 경북 문경시 중앙로 15 1층 (지번: 모전동 81-89)
# Old addresses found earlier: "경북 문경시 중앙로 156", "경북 문경시 중앙로 15", "경북 문경시 모전동 81-89"
# Actually, "경북 문경시 중앙로 156" seems to be the main culprit of being wrong if it points to a different location.

count = 0
for s in data:
    if '왕대박' in s['n'] and '문경' in s['a']:
        # Update address to the most accurate one
        # If it was "중앙로 156", it's definitely wrong according to user.
        # User image shows "중앙로 15 1층"
        s['a'] = "경북 문경시 중앙로 15"
        count += 1

if count > 0:
    with open('lotto_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Updated {count} records in lotto_data.json")
else:
    print("No matching records found to update.")
