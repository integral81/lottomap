
import json
import os

file_path = 'c:\\Users\\이승민\\OneDrive\\Desktop\\KINOV_Lotto_Map\\lotto_data.json'

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

count = 0
for entry in data:
    if entry.get('n') == '인터넷 복권판매사이트':
        entry['a'] = "서울특별시 서초구 남부순환로 2423 (서초동, 한원빌딩) 4층"
        entry['lat'] = 37.481793
        entry['lng'] = 127.015371
        # Ensure it's not marked as closed if it was
        if 'closed' in entry:
            del entry['closed']
        count += 1

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Updated {count} entries.")
