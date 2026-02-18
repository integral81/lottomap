import json
import os

file_path = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js'
backup_path = file_path + '.bak'

# Create backup
if not os.path.exists(backup_path):
    import shutil
    shutil.copy2(file_path, backup_path)

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the window.lottoData = prefix
prefix = 'window.lottoData = '
json_str = content.replace(prefix, '').strip()
if json_str.endswith(';'):
    json_str = json_str[:-1]

data = json.loads(json_str)

# Targets to mark as closed
closed_targets = [
    "동소문로20길 28-4",
    "낙동대로 1704"
]

modified_count = 0
for entry in data:
    for target in closed_targets:
        if target in entry.get('a', ''):
            if not entry.get('closed'):
                entry['closed'] = True
                modified_count += 1

print(f"Modified {modified_count} entries.")

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(prefix + json.dumps(data, ensure_ascii=False) + ';')
