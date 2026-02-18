import json
import glob
import os

target_file = 'lotto_data.json'

def load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def main():
    print("Loading target data...")
    with open(target_file, 'r', encoding='utf-8') as f:
        target_data = json.load(f)
        
    # Identify missing
    missing_targets = []
    for s in target_data:
        # Check if wins >= 3 and missing POV
        wins = s.get('wins', 0)
        try: wins = int(wins)
        except: wins = 0
        
        if not s.get('pov') or not s.get('panoid'):
            missing_targets.append(s)
            
    print(f"Found {len(missing_targets)} shops missing POV in current data.")
    
    if not missing_targets:
        print("Nothing to restore.")
        return

    # Build Lookup from ALL backups
    backup_files = glob.glob('*.json') + glob.glob('*.bak')
    # Prioritize recent
    backup_files.sort(key=os.path.getmtime, reverse=True)
    
    pov_lookup = {} # Key: "Name|City" -> POV Data
    
    print("Building Recovery Database from backups...")
    for bf in backup_files:
        if bf == target_file: continue
        data = load_json(bf)
        if not isinstance(data, list): continue
        
        for s in data:
            if s.get('pov') and s.get('panoid'):
                n = s.get('n', '').strip()
                a = s.get('a', '').strip()
                city = a.split(' ')[0] if ' ' in a else a
                
                key1 = f"{n}|{city}" # Most robust
                key2 = n # Fallback for unique names
                
                if key1 not in pov_lookup:
                    pov_lookup[key1] = s
                if key2 not in pov_lookup:
                    pov_lookup[key2] = s
                    
    print(f"Database built with {len(pov_lookup)} unique POV entries.")
    
    # Apply
    restored_count = 0
    for t in missing_targets:
        n = t.get('n', '').strip()
        a = t.get('a', '').strip()
        city = a.split(' ')[0] if ' ' in a else a
        
        key1 = f"{n}|{city}"
        key2 = n
        
        match = None
        if key1 in pov_lookup:
            match = pov_lookup[key1]
        elif key2 in pov_lookup:
            match = pov_lookup[key2]
            
        if match:
            t['pov'] = match['pov']
            t['panoid'] = match['panoid']
            # Sync ID
            if 'id' not in t['pov']:
                t['pov']['id'] = t['panoid']
            restored_count += 1
            # print(f"Restored: {n}")
            
    print(f"Restored {restored_count} shops from backups.")
    
    if restored_count > 0:
        with open(target_file, 'w', encoding='utf-8') as f:
            json.dump(target_data, f, ensure_ascii=False, indent=4)
        with open(target_file.replace('.json', '.js'), 'w', encoding='utf-8') as f:
             f.write('const lottoData = ' + json.dumps(target_data, ensure_ascii=False) + ';')

if __name__ == "__main__":
    main()
