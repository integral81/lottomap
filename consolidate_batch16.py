import json

f_json = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json'
f_js = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js'

with open(f_json, 'r', encoding='utf-8') as f:
    data = json.load(f)

targets = [
    { "name": "복권판매소", "addr": "국채보상로 438" },
    { "name": "청구마트", "addr": "검단로 34" },
    { "name": "월드복권", "addr": "북비산로 98" },
    { "name": "대흥당", "addr": "관통로 102" }
]

new_data = []
seen_targets = { t['name']: False for t in targets }
removed_count = 0

for s in data:
    is_target = False
    for t in targets:
        if t['name'] in s.get('n', '') and t['addr'] in s.get('a', ''):
            is_target = True
            if not seen_targets[t['name']]:
                # Keep the first one
                new_data.append(s)
                seen_targets[t['name']] = True
            else:
                # Discard duplicates
                removed_count += 1
            break # Stop checking other targets for this record
    
    if not is_target:
        new_data.append(s)

if removed_count > 0:
    with open(f_json, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=4)
    
    with open(f_js, 'w', encoding='utf-8') as f:
        f.write('const lottoData = ' + json.dumps(new_data, ensure_ascii=False) + ';')
    
    print(f"Consolidation complete. Removed {removed_count} duplicate records.")
else:
    print("No duplicates removed.")
