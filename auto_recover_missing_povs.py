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
    # 1. Identify missing POV shops in current data
    with open(target_file, 'r', encoding='utf-8') as f:
        current_data = json.load(f)
    
    missing_targets = []
    for s in current_data:
        # Criteria: 3+ wins OR manually flagged, AND missing POV
        # We'll just look for any shop with wins >= 3 missing POV
        wins = s.get('wins', 0)
        try:
            wins = int(wins)
        except:
            wins = 0
            
        if wins >= 3 and (not s.get('pov') or not s.get('panoid')):
            missing_targets.append(s)
            
    print(f"Found {len(missing_targets)} shops missing POV in current data.")
    
    # 2. Build a lookup of (Name, Address) -> POV from ALL backups
    backup_files = glob.glob('*.json') + glob.glob('*.bak')
    # Prioritize recent backups
    backup_files.sort(key=os.path.getmtime, reverse=True)
    
    pov_cache = {} # Key: "Name|AddressPrefix" -> POV
    
    print("Scanning backups for POV data...")
    for bf in backup_files:
        if bf == target_file: continue
        # Skip huge files if too slow? No, read them.
        print(f"  Scanning {bf}...")
        data = load_json(bf)
        if not isinstance(data, list): continue
        
        for s in data:
            if s.get('pov') and s.get('panoid'):
                name = s.get('n', '').strip()
                addr = s.get('a', '').strip()
                # Create flexible keys
                keys = [
                    f"{name}|{addr}",
                    f"{name}|{addr.split(' ')[0]} {addr.split(' ')[1]}", # City match
                    name # Just name (risky but useful for unique names)
                ]
                
                for k in keys:
                    if k not in pov_cache:
                        pov_cache[k] = s
    
    # 3. Apply to missing targets
    restored_count = 0
    for t in missing_targets:
        name = t.get('n', '').strip()
        addr = t.get('a', '').strip()
        
        # Try keys in order of specificity
        keys = [
            f"{name}|{addr}",
            f"{name}|{addr.split(' ')[0]} {addr.split(' ')[1]}",
            name
        ]
        
        match = None
        for k in keys:
            if k in pov_cache:
                match = pov_cache[k]
                break
        
        if match:
             t['pov'] = match['pov']
             t['panoid'] = match['panoid']
             restored_count += 1
             print(f"Restored POV for '{name}' from backup!")
        else:
             print(f"Could not find POV for '{name}' in any backup.")

    # 4. Save
    if restored_count > 0:
        print(f"Saving {restored_count} restored POVs...")
        with open(target_file, 'w', encoding='utf-8') as f:
            json.dump(current_data, f, ensure_ascii=False, indent=4)
        
        with open(target_file.replace('.json', '.js'), 'w', encoding='utf-8') as f:
            f.write('const lottoData = ' + json.dumps(current_data, ensure_ascii=False) + ';')
    else:
        print("No POVs restored.")

if __name__ == "__main__":
    main()
