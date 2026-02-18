import json

# Target Data provided by user
targets = [
    { "name": "로또25시", "addr": "울산 남구 수암로288번길 1", "panoid": 1201947010, "pov": { "pan": 125.20, "tilt": 5.98, "zoom": -3 } },
    { "name": "대박명당", "addr": "울산 북구 매곡로 93-2", "panoid": 1201865388, "pov": { "pan": 309.05, "tilt": 5.91, "zoom": 0 } }
]

f_json = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json'
f_js = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js'

def main():
    with open(f_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updated_count = 0
    
    for t in targets:
        t_name = t['name']
        t_addr_key = t['addr'].split(' ')[2] # e.g. "수암로288번길", "매곡로"
        
        print(f"Applying POV to ALL entries of: {t_name} ({t['addr']})")
        
        for s in data:
            # Check Name MATCH
            if s.get('n') == t_name:
                # Check Address partial match to distinguish from other branches
                if t_addr_key in s.get('a', ''):
                    # APPLY POV
                    s['panoid'] = t['panoid']
                    # Construct valid POV object with ID
                    p = t['pov'].copy()
                    p['id'] = t['panoid']
                    s['pov'] = p
                    
                    updated_count += 1
                    # print(f"  -> Updated round {s.get('r')}")

    print(f"Total updated entries: {updated_count}")
    
    # Save
    with open(f_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    with open(f_js, 'w', encoding='utf-8') as f:
        f.write('const lottoData = ' + json.dumps(data, ensure_ascii=False) + ';')

if __name__ == "__main__":
    main()
