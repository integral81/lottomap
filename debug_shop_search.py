import json
import glob
import os

target = "세븐일레븐부산온천장역점"
keyword = "온천장"

# 1. Check Data
try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"Checking '{target}' in data...")
    found = [s for s in data if keyword in s.get('n', '')]
    for s in found:
        print(f"  Found: {s.get('n')} (Wins: {s.get('wins')}) POV: {s.get('pov')}")
except Exception as e:
    print(f"Error reading data: {e}")

# 2. Check Scripts
print(f"\nSearching '{keyword}' in scripts...")
for py_file in glob.glob('apply_batch*.py'):
    try:
        with open(py_file, 'r', encoding='utf-8') as f:
            if keyword in f.read():
                print(f"  Match in: {py_file}")
    except:
        pass
