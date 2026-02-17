import json

def main():
    f_json = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json'
    f_js = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js'
    
    with open(f_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Check specifically for troublesome shops
    trouble_shops = ['세븐일레븐부산온천장역점', '제철로또대리점', 'Goodday복권전문점', '완월로또', '채널큐', '해피복권']
    
    for t in trouble_shops:
        print(f"\n--- Checking {t} ---")
        matches = [s for s in data if t in s.get('n', '')]
        
        # Find POV source
        source_pov = None
        source_panoid = None
        for s in matches:
             if s.get('pov') and s.get('panoid'):
                 source_pov = s['pov']
                 source_panoid = s['panoid']
                 print(f"  Found Source: {s.get('n')} (Round {s.get('r')})")
                 break
        
        if source_pov:
            count = 0
            for s in matches:
                if not s.get('pov'):
                    s['pov'] = source_pov
                    s['panoid'] = source_panoid
                    count += 1
                    print(f"  -> Propagated to {s.get('n')} (Round {s.get('r')})")
            print(f"  Total propagated for {t}: {count}")
        else:
            print(f"  No POV source found for {t}")

    # General Propagation (Exact Name Match)
    print("\n--- General Propagation (Exact Name Match) ---")
    by_name = {}
    for s in data:
        n = s.get('n', '')
        if n not in by_name: by_name[n] = []
        by_name[n].append(s)
        
    gen_count = 0
    for n, group in by_name.items():
        if len(group) < 2: continue
        
        src_pov = None
        src_panoid = None
        for s in group:
            if s.get('pov'):
                src_pov = s['pov']
                src_panoid = s.get('panoid')
                break
        
        if src_pov:
            for s in group:
                if not s.get('pov'):
                    s['pov'] = src_pov
                    if src_panoid: s['panoid'] = src_panoid
                    gen_count += 1
                    
    print(f"General Propagation Count: {gen_count}")

    # Save
    with open(f_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    with open(f_js, 'w', encoding='utf-8') as f:
        f.write('const lottoData = ' + json.dumps(data, ensure_ascii=False) + ';')

if __name__ == "__main__":
    main()
