import json
import glob
import os

target_backup = 'lotto_data_backup_sky_lotto_fix_20260216_121619.json'
target_name = "세븐일레븐부산온천장역점"

print(f"Extracting from {target_backup}...")

try:
    with open(target_backup, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    found = [s for s in data if target_name in s.get('n', '')]
    if found:
        print(f"Found {len(found)} entries.")
        for s in found:
            print(f"POV: {s.get('pov')}")
            if s.get('pov'):
                # Generate a repair script or just do it here?
                # We will output a JSON snippet to be used.
                print(f"RECOVERY_DATA: {json.dumps(s)}")
    else:
        print("Not found in backup.")
        
except Exception as e:
    print(f"Error: {e}")

print("\nSearching for '온천장' in .py files...")
for py in glob.glob('*.py'):
    try:
        with open(py, 'r', encoding='utf-8') as f:
            if '온천장' in f.read():
                print(f"Found keyword in {py}")
    except:
        pass
