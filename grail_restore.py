import json
import glob
import os

target_file = 'lotto_data.json'
grail_backup = 'lotto_data.current.bak' # Derived from partial success logs

print(f"Restoring from {grail_backup} (The Holy Grail)...")

with open(grail_backup, 'r', encoding='utf-8') as f:
    grail_data = json.load(f)
    
with open(target_file, 'r', encoding='utf-8') as f:
    current_data = json.load(f)
    
# Build Map
pov_map = {}
for s in grail_data:
    if s.get('pov') and s.get('panoid'):
        n = s.get('n', '').strip()
        a = s.get('a', '').strip()
        
        # Keys
        pov_map[n] = s
        pov_map[f"{n}|{a}"] = s
        pov_map[f"{n}|{a.split(' ')[0]}"] = s # City

restored = 0
for s in current_data:
    if not s.get('pov'):
        n = s.get('n', '').strip()
        a = s.get('a', '').strip()
        city = a.split(' ')[0] if ' ' in a else a
        
        match = None
        # Try keys
        if n in pov_map: match = pov_map[n]
        elif f"{n}|{a}" in pov_map: match = pov_map[f"{n}|{a}"]
        elif f"{n}|{city}" in pov_map: match = pov_map[f"{n}|{city}"]
        
        if match:
            s['pov'] = match['pov']
            s['panoid'] = match['panoid']
            if 'id' not in s['pov']: s['pov']['id'] = s['panoid']
            restored += 1

print(f"Restored {restored} shops from {grail_backup}")

if restored > 0:
    with open(target_file, 'w', encoding='utf-8') as f:
        json.dump(current_data, f, ensure_ascii=False, indent=4)
    with open(target_file.replace('.json', '.js'), 'w', encoding='utf-8') as f:
        f.write('const lottoData = ' + json.dumps(current_data, ensure_ascii=False) + ';')
