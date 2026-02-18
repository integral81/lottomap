import json
import glob
import os

target_name = "세븐일레븐부산온천장역점"
print(f"Searching for '{target_name}' POV in all files...")

files = glob.glob('*.json') + glob.glob('*.bak')

good_backups = []

for fp in files:
    try:
        with open(fp, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        found = False
        for s in data:
            if target_name in s.get('n', ''):
                if s.get('pov'):
                    print(f"[{fp}] FOUND! POV: {s['pov']}")
                    found = True
                    break # One match per file is enough to check validity
        
        if found:
            good_backups.append(fp)
            
    except:
        pass

print("\n--- Summary ---")
if good_backups:
    print(f"Best backup candidates: {good_backups}")
    # Recommend restoring from the largest/latest of these?
    latest = max(good_backups, key=os.path.getmtime)
    print(f"Latest good backup: {latest}")
else:
    print("FATAL: No backup contains POV for Se7en Busan.")
