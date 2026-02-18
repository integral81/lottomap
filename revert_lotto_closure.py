import json
import os

file_path = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js'
prefix = 'window.lottoData = '

# Read existing file
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

json_str = content.replace(prefix, '').strip()
if json_str.endswith(';'):
    json_str = json_str[:-1]

data = json.loads(json_str)

# Target to revert (mark as OPEN)
revert_target = "낙동대로 1704"
found = False

for entry in data:
    if revert_target in entry.get('a', ''):
        if entry.get('closed'):
            del entry['closed']
            found = True

if found:
    print(f"Reverted closure for {revert_target}.")
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(prefix + json.dumps(data, ensure_ascii=False) + ';')
else:
    print(f"Could not find closed entry for {revert_target}.")
