import json

f_json = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json'
f_js = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js'

with open(f_json, 'r', encoding='utf-8') as f:
    data = json.load(f)

updated_count = 0
for s in data:
    # If it has panoid but pov is missing 'id', add it for admin_pov.html compatibility
    if s.get('panoid') and s.get('pov'):
        if not s['pov'].get('id'):
            s['pov']['id'] = s['panoid']
            updated_count += 1
    # If it has pov with 'id' but no root 'panoid', sync root 'panoid'
    elif s.get('pov') and isinstance(s['pov'], dict) and s['pov'].get('id'):
        if not s.get('panoid'):
            s['panoid'] = s['pov']['id']
            updated_count += 1

if updated_count > 0:
    with open(f_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    with open(f_js, 'w', encoding='utf-8') as f:
        f.write('const lottoData = ' + json.dumps(data, ensure_ascii=False) + ';')
    
    print(f"Standardized {updated_count} records.")
else:
    print("No records needed standardization.")
