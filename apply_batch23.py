import json
import os

# Batch 23 Data (4 items)
batch23 = [
    { "name": "로또25시", "addr": "울산 남구 수암로288번길 1", "panoid": 1201947010, "pov": { "pan": 123.44, "tilt": 0.78, "zoom": -3 } },
    { "name": "대박명당", "addr": "울산 북구 매곡로 93-2", "panoid": 1201865388, "pov": { "pan": 289.58, "tilt": 4.05, "zoom": 2 } },
    { "name": "로또슈퍼", "addr": "광주 서구 상일로 37 모아제일아파트상가1층102호", "panoid": 1200649226, "pov": { "pan": 18.60, "tilt": 2.88, "zoom": 2 } },
    { "name": "왕대박", "addr": "대구 남구 대명로 51 A동1층7호", "panoid": 1201386552, "pov": { "pan": 343.37, "tilt": 8.53, "zoom": 0 } }
]

f_json = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json'
f_js = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js'

def load_data():
    with open(f_json, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(f_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    with open(f_js, 'w', encoding='utf-8') as f:
        f.write('const lottoData = ' + json.dumps(data, ensure_ascii=False) + ';')

def main():
    data = load_data()
    updated_count = 0
    not_found = []

    print(f"Total shops before: {len(data)}")

    for b in batch23:
        target_name = b['name']
        found = False
        
        # Address matching for generic names
        addr_keyword = b['addr'].split(' ')[1]  # Gu/Gun level

        for s in data:
            n1 = target_name.replace(' ', '')
            n2 = s.get('n', '').replace(' ', '')
            
            if (n1 in n2 or n2 in n1):
                 # Safety check for "왕대박" generic name
                 if "왕대박" in n1 and addr_keyword not in s.get('a', ''):
                     continue

                 s['panoid'] = b['panoid']
                 pov_data = b['pov'].copy()
                 pov_data['id'] = b['panoid']
                 s['pov'] = pov_data
                 updated_count += 1
                 found = True
                 print(f"Updated: {s['n']} ({s.get('a')})")
                 break
        
        if not found:
            not_found.append(b['name'])
            print(f"[WARN] Not found: {target_name}")

    save_data(data)
    print(f"Batch 23: Updated {updated_count} / {len(batch23)} shops.")
    if not_found:
        print("Missing:", not_found)

if __name__ == "__main__":
    main()
