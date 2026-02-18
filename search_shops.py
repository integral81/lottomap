import json
import re

file_path = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the window.lottoData = prefix
json_str = content.replace('window.lottoData = ', '').strip()
if json_str.endswith(';'):
    json_str = json_str[:-1]

data = json.loads(json_str)

targets = [
    "덕천동"
]

results = []
for entry in data:
    for target in targets:
        if target in entry.get('a', ''):
            results.append(entry)

print(json.dumps(results, ensure_ascii=False, indent=2))
