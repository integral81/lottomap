import json

f_json = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json'
f_js = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js'

with open(f_json, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Target to consolidate
target_name = "춘향로또"
target_addr = "동림로 102-1"

# Filter out duplicates
new_data = []
seen_chunhyang = False

removed_count = 0

for s in data:
    if target_name in s.get('n', '') and target_addr in s.get('a', ''):
        if not seen_chunhyang:
            # Keep the first one
            new_data.append(s)
            seen_chunhyang = True
        else:
            # Skip subsequent duplicates
            removed_count += 1
    else:
        new_data.append(s)

if removed_count > 0:
    with open(f_json, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=4)
    
    with open(f_js, 'w', encoding='utf-8') as f:
        f.write('const lottoData = ' + json.dumps(new_data, ensure_ascii=False) + ';')
    
    print(f"Removed {removed_count} duplicate entries for '{target_name}'.")
else:
    print(f"No duplicates found for '{target_name}'.")
