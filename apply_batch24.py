import json
import os

# Batch 24 Data (3 items)
batch24 = [
    { "name": "역전로또", "addr": "경북 구미시 구미중앙로 72", "panoid": 1165801454, "pov": { "pan": 243.35, "tilt": 0.68, "zoom": 3 } },
    { "name": "왕대박로또", "addr": "전북 전주시 덕진구 만성북로 19 조은 프라자 106호", "panoid": 1205358265, "pov": { "pan": 25.86, "tilt": 0.39, "zoom": -1 } },
    { "name": "중앙로또", "addr": "강원 양구군 장터길 27 1층 중앙청과", "panoid": 1196703897, "pov": { "pan": 214.37, "tilt": 4.88, "zoom": -1 } }
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

    for b in batch24:
        target_name = b['name']
        found = False
        
        # Address matching part (City/Gu)
        addr_parts = b['addr'].split(' ')
        addr_keyword = addr_parts[1] if len(addr_parts) > 1 else "" 
        
        for s in data:
            # Name check
            if target_name.replace(' ', '') in s.get('n', '').replace(' ', ''):
                 # Address check for safety
                 if addr_keyword in s.get('a', ''):
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
            # Retry with broader search for "왕대박로또" vs "왕대박" 
            # (But wait, we have distinct "왕대박" in Daegu and "왕대박로또" in Jeonju)
            print(f"[WARN] Not found: {target_name}")

    save_data(data)
    print(f"Batch 24: Updated {updated_count} / {len(batch24)} shops.")
    if not_found:
        print("Missing:", not_found)

if __name__ == "__main__":
    main()
