import json
import glob
import re

# Target File
target_file = 'lotto_data.json'

def load_json(path, encoding='utf-8'):
    try:
        with open(path, 'r', encoding=encoding) as f:
            return json.load(f)
    except Exception:
        return None

def main():
    print("Loading Target Data...")
    current_data = load_json(target_file)
    if not current_data:
        print("Failed to load target file.")
        return

    # Identify Candidates: Wins=3 and NO POV
    candidates = []
    for s in current_data:
        wins = s.get('wins', 0)
        try: wins = int(wins)
        except: wins = 0
        
        # Determine if incomplete
        has_pov = s.get('pov') and (s.get('pov').get('id') or s.get('pov').get('panoid') or s.get('panoid'))
        
        if wins == 3 and not has_pov:
            candidates.append(s)
            
    print(f"Found {len(candidates)} candidates (Wins=3, Missing POV) in current data.")
    
    if len(candidates) == 0:
        print("No candidates to restore.")
        return

    # Load All Backups (Try multiple encodings)
    backup_files = glob.glob('*.json') + glob.glob('*.bak')
    encodings = ['utf-8', 'cp949', 'euc-kr', 'utf-16']
    
    # Pre-load backup data to avoid re-reading
    all_backups_data = []
    for fp in backup_files:
        if fp == target_file: continue
        
        loaded = False
        for enc in encodings:
            data = load_json(fp, enc)
            if data and isinstance(data, list) and len(data) > 0:
                # Check if it has ANY POV
                has_any_pov = any(s.get('pov') for s in data)
                if has_any_pov:
                    all_backups_data.append({'file': fp, 'data': data})
                    loaded = True
                    break
        if not loaded:
            # print(f"Skipping {fp} (Empty or invalid)")
            pass
            
    print(f"Loaded {len(all_backups_data)} valid backup files.")
    
    # Restore Logic: Address Matching
    restored_count = 0
    
    for cand in candidates:
        name = cand.get('n', '')
        addr = cand.get('a', '')
        
        # Tokenize Address: Look for the number part e.g. "156-1", "1428", "315"
        # Heuristic: The last purely numeric/dash token in address is usually the lot number
        # e.g. "부산 동래구 온천동 156-1" -> "156-1"
        # "광주 광산구 수완동 1428 세븐일레븐내" -> "1428"
        
        tokens = addr.split()
        search_token = None
        for t in reversed(tokens):
             # Remove non-digit/dash chars?
             clean = re.sub(r'[^\d-]', '', t)
             if len(clean) >= 2: # At least 2 digits
                 if '-' in clean or len(clean) >= 3: # Prefer 156-1 or 1428 over "1"
                     search_token = clean
                     break
        
        if not search_token:
            print(f"Skipping {name} ({addr}) - No robust address token found.")
            continue
            
        # Search match in backups
        found_pov = None
        found_source = None
        
        for backup in all_backups_data:
            b_data = backup['data']
            for b_item in b_data:
                # Check Address Token inclusion
                # Also handle encoding of address in backup?
                # We loaded JSON objects, so b_item['a'] is a string (hopefully decoded correctly)
                b_addr = b_item.get('a', '')
                if search_token in b_addr:
                    # Potential Match. Confirm with Name partial match or City match?
                    # The user said name encoding might be issue.
                    # Rely on Address Token + Win Count similarity? Or just Token?
                    # Let's check POV existence
                    if b_item.get('pov') and b_item.get('panoid'):
                         # Strong candidate
                         # Check if names are "similar" length? 
                         # Or just trust the address token uniqueness for now.
                         # Let's print for verification log
                         print(f"Match found for '{name}' ({addr}) using token '{search_token}' in {backup['file']}")
                         # print(f"  Backup Entry: {b_item.get('n')} / {b_item.get('a')}")
                         found_pov = b_item['pov']
                         found_panoid = b_item['panoid']
                         found_source = backup['file']
                         break
            if found_pov: break
            
        if found_pov:
            cand['pov'] = found_pov
            cand['panoid'] = found_panoid
            # Ensure ID
            if 'id' not in cand['pov']: cand['pov']['id'] = found_panoid
            restored_count += 1
            print(f"-> Restored POV for {name}")
        else:
            print(f"No match for {name} ({addr}) [Token: {search_token}]")

    print(f"\nTotal Restored: {restored_count}")
    
    # Save
    if restored_count > 0:
        with open(target_file, 'w', encoding='utf-8') as f:
            json.dump(current_data, f, ensure_ascii=False, indent=4)
        with open('lotto_data.js', 'w', encoding='utf-8') as f:
            f.write('const lottoData = ' + json.dumps(current_data, ensure_ascii=False) + ';')
            
if __name__ == "__main__":
    main()
