import json
import os

# Batch 25 Data (3 items)
batch25 = [
    { "name": "보건약국", "addr": "강원 원주시 단계로 293", "panoid": 1202719159, "pov": { "pan": 240.68, "tilt": 5.77, "zoom": -3 } },
    { "name": "왕대박복권전문점", "addr": "강원 동해시 중앙로 234 이주민상가 1층 14호", "panoid": 1152865954, "pov": { "pan": 81.33, "tilt": -6.64, "zoom": 1 } },
    { "name": "CU(평택중앙점)", "addr": "경기 평택시 중앙로 95", "panoid": 1198424296, "pov": { "pan": 234.33, "tilt": 1.48, "zoom": 1 } }
]

f_json = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json'
f_js = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js'

def load_data():
    with open(f_json, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    # Save JSON
    with open(f_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    # Save JS
    with open(f_js, 'w', encoding='utf-8') as f:
        f.write('const lottoData = ' + json.dumps(data, ensure_ascii=False) + ';')

def main():
    try:
        data = load_data()
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    updated_count = 0
    not_found = []

    print(f"Total shops before: {len(data)}")

    for b in batch25:
        target_name = b['name']
        found = False
        
        # Simple Logic
        addr_keyword = b['addr'].split(' ')[2] if len(b['addr'].split(' ')) > 2 else ""

        for s in data:
            if target_name in s.get('n', ''):
                if addr_keyword == "" or addr_keyword in s.get('a', ''):
                     s['panoid'] = b['panoid']
                     pov_data = b['pov'].copy()
                     pov_data['id'] = b['panoid']
                     s['pov'] = pov_data
                     updated_count += 1
                     found = True
                     print(f"Updated: {s['n']}")
                     break
        
        if not found:
            not_found.append(b['name'])
            print(f"[WARN] Not found: {target_name}")

    save_data(data)
    print(f"Batch 25: Updated {updated_count} / {len(batch25)} shops.")
    if not_found:
        print("Missing:", not_found)

if __name__ == "__main__":
    main()
