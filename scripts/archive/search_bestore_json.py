import json

lotto_data_path = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json"

search_name = "베스토아"
search_addresses = ["동서대로 1689", "용전동 63-3"]

with open(lotto_data_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

matches = []
for entry in data:
    name_match = search_name in entry.get('n', '')
    addr_match = any(addr in entry.get('a', '') for addr in search_addresses)
    
    if name_match and addr_match:
        matches.append(entry)

print(f"Total matches found in lotto_data.json: {len(matches)}")
for m in matches:
    print(f"Round {m.get('r')}: {m.get('n')} - {m.get('a')} ({m.get('m')})")
