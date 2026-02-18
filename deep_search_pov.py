import json
import glob
import os

targets = ["세븐일레븐부산온천장역점", "세븐일레븐 수완점", "베스트원", "춘향로또"]

print("Mining all JSON files for POV data...")
json_files = glob.glob('*.json') + glob.glob('*.bak')

sources = {}

for fpth in json_files:
    try:
        with open(fpth, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        for s in data:
            name = s.get('n', '')
            for t in targets:
                if t in name:
                    if s.get('pov') and s.get('panoid'):
                        print(f"[{fpth}] FOUND POV for '{name}'")
                        if t not in sources:
                            sources[t] = s
                    else:
                        pass
                        # print(f"[{fpth}] Found '{name}' but NO POV")
    except:
        pass

print("\nMining admin_targets_history.txt...")
try:
    with open('admin_targets_history.txt', 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        print(f"Read {len(lines)} lines from history.")
        for line in lines:
            for t in targets:
                if t in line:
                    print(f"[HISTORY] Found '{t}' in line: {line.strip()[:100]}...")
except FileNotFoundError:
    print("admin_targets_history.txt not found.")

if sources:
    print("\nRestoration Plan:")
    for t, s in sources.items():
        print(f"  Restore '{t}' using POV from backup.")
else:
    print("\nNo valid POV source found in any file.")
