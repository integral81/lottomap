import json
import glob
import re
import os

# Regex to capture JSON-like objects in Python code
# We look for 'name': '...', 'pov': { ... } pattern
# This is a bit complex to regex perfectly, but we can try to find valid JSON-dict strings or evaluate python code structures.
# Safest is to parsing the python AST? No, files might be partial.
# Let's try text processing.

def extract_povs_from_file(filepath):
    extracted = []
    try:
        # Try UTF-8 then CP949
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            with open(filepath, 'r', encoding='cp949') as f:
                content = f.read()
                
        # Look for "pov": { ... } blocks
        # And capture slightly before it to get "name"
        
        # Strategy: Evaluate the file? Dangerous.
        # Strategy: Import the file? Only if it's a module.
        # Strategy: Text parsing.
        
        # Many files look like:
        # batch = [ { "name": "...", "addr": "...", ... "pov": {...} }, ... ]
        
        # Let's find all occurrences of dictionary-like strings.
        # We'll use a simple approach: split by "pov": or 'pov':
        
        parts = re.split(r'[\"\']pov[\"\']\s*:\s*\{', content)
        if len(parts) < 2:
            return []
            
        for i in range(1, len(parts)):
            # The part AFTER "pov": { is the POV body. 
            # We need to parse until '}'.
            body_chunk = parts[i]
            bracket_balance = 1
            pov_str = "{"
            
            for char in body_chunk:
                if char == '{': bracket_balance += 1
                if char == '}': bracket_balance -= 1
                pov_str += char
                if bracket_balance == 0:
                    break
            
            # Now we have the POV object string, e.g. { "pan": ... }
            try:
                # Relaxed JSON parsing (python dict literal to json)
                # handle unquoted keys if necessary, but usually they are quoted in these files
                pov_obj = eval(pov_str) 
            except:
                continue
                
            # Now find the NAME associated with this POV.
            # Look backwards in parts[i-1] for "name": "..." or 'name': '...'
            pre_chunk = parts[i-1]
            
            # Reverse search for name
            name_match = re.search(r'[\"\']name[\"\']\s*:\s*[\"\'](.*?)[\"\']', pre_chunk[::-1])
            if name_match:
                # Reverse the captured name back
                name = name_match.group(1)[::-1]
                
                # Also try to get panoid
                panoid_match = re.search(r'[\"\']panoid[\"\']\s*:\s*(\d+)', pre_chunk[::-1])
                panoid = None
                if panoid_match:
                    panoid = int(panoid_match.group(1)[::-1])
                
                # Also try to get zoom/tilt/pan from pov_obj if valid
                if isinstance(pov_obj, dict):
                    extracted.append({
                        'name': name,
                        'pov': pov_obj,
                        'panoid': panoid,
                        'source': filepath
                    })
    except Exception as e:
        print(f"Skipping {filepath}: {e}")
        
    return extracted

def main():
    print("Mining POVs from ALL .py files...")
    all_extracted = []
    
    # Target specific files we know contain data
    target_files = glob.glob('apply_batch*.py') + \
                   glob.glob('register_batch*.py') + \
                   glob.glob('update_*.py') + \
                   glob.glob('check_*.py')
                   
    # Unique files
    target_files = list(set(target_files))
    
    for py_file in target_files:
        result = extract_povs_from_file(py_file)
        if result:
            print(f"  Found {len(result)} POVs in {py_file}")
            all_extracted.extend(result)
            
    print(f"Total extracted candidates: {len(all_extracted)}")
    
    # Load Main Data
    json_path = 'lotto_data.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        lotto_data = json.load(f)
        
    updated_count = 0
    
    # Create valid POV lookup
    # Key: Name -> POV Data
    pov_lookup = {}
    for item in all_extracted:
        # filter bad names
        n = item['name'].strip()
        if len(n) > 1:
            pov_lookup[n] = item
            
    # Apply to Lotto Data
    for s in lotto_data:
        # Condition: Shop has NO POV (or check matches)
        # Verify if Shop is in "missing" list (e.g. 3 wins) -> The user says 145 items are lingering.
        # We should probably apply to ANY shop matching the name if it doesn't have a pov OR even if it does (to restore newer version)
        # But safest is: If current POV is missing, apply.
        
        current_pov = s.get('pov')
        name = s.get('n', '').strip()
        
        if not current_pov and name in pov_lookup:
            cand = pov_lookup[name]
            # Verify address match if possible? 
            # User said "Name similarity caused deletion", so let's be careful but aggressive given the user's request "Process EVERYTHING"
            
            s['pov'] = cand['pov']
            if cand['panoid']:
                s['panoid'] = cand['panoid']
                s['pov']['id'] = cand['panoid'] # Ensure ID inside POV
            
            updated_count += 1
            print(f"Restored POV for: {name} (from {cand['source']})")
            
    if updated_count > 0:
        print(f"Saving {updated_count} restored shops to {json_path}")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(lotto_data, f, ensure_ascii=False, indent=4)
        with open('lotto_data.js', 'w', encoding='utf-8') as f:
            f.write('const lottoData = ' + json.dumps(lotto_data, ensure_ascii=False) + ';')
    else:
        print("No matches found to restore.")

if __name__ == "__main__":
    main()
