import json

# Group shops by "Name + Address Prefix"
# If one has POV, copy to others.

def normalize_key(s):
    n = s.get('n', '').strip()
    a = s.get('a', '').strip()
    # Simple key: Name + First 2 words of Address
    a_parts = a.split(' ')
    if len(a_parts) >= 2:
        a_key = " ".join(a_parts[:2])
    else:
        a_key = a
    return f"{n}|{a_key}"

def main():
    f_json = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json'
    f_js = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js'
    
    with open(f_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 1. Group by Key
    groups = {}
    for s in data:
        k = normalize_key(s)
        if k not in groups:
            groups[k] = []
        groups[k].append(s)
        
    updated_count = 0
    shops_updated = 0
    
    # 2. Iterate Groups
    for k, check_shops in groups.items():
        # Find POV source
        source_pov = None
        source_panoid = None
        
        # Priority: Has POV object AND Panoid ID
        for s in check_shops:
            if s.get('pov') and s.get('panoid'):
                source_pov = s['pov']
                source_panoid = s['panoid']
                break
        
        if not source_pov:
            # Maybe just panoid?
            for s in check_shops:
                if s.get('panoid'):
                    source_panoid = s['panoid']
                    # Construct minimal POV if missing?
                    # Or skip if no POV object?
                    # Usually POV object is needed for roadview.
                    # If existing admin uses only panoid, maybe OK.
                    # But let's prioritize full object.
                    break
        
        # 3. Propagate
        if source_pov and source_panoid:
            for s in check_shops:
                # If target lacks valid POV, copy it
                if not s.get('pov') or not s.get('panoid'):
                    s['pov'] = source_pov
                    s['panoid'] = source_panoid
                    updated_count += 1
            if updated_count > 0:
                shops_updated += 1
                
    print(f"Propagated POV to {updated_count} entries across {shops_updated} unique shop groups.")
    
    # 4. Save
    with open(f_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    with open(f_js, 'w', encoding='utf-8') as f:
        f.write('const lottoData = ' + json.dumps(data, ensure_ascii=False) + ';')

if __name__ == "__main__":
    main()
