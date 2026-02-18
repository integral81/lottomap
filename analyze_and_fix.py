import json
import glob
import os

# 1. Register '대흥당' (User provided)
target = { "name": "대흥당", "addr": "전북 정읍시 관통로 102", "panoid": 1183542559, "pov": { "pan": 347.29, "tilt": 2.37, "zoom": 2 } }
db_file = 'lotto_data.json'

with open(db_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

updated = False
for s in data:
    if "대흥당" in s['n']:
        s['panoid'] = target['panoid']
        s['pov'] = target['pov'].copy()
        s['pov']['id'] = target['panoid']
        updated = True
        print(f"Registered POV for: {s['n']} (Wins: {s.get('wins')})")

if updated:
    with open(db_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    with open('lotto_data.js', 'w', encoding='utf-8') as f:
        f.write('const lottoData = ' + json.dumps(data, ensure_ascii=False) + ';')
    print("Saved '대흥당' update.")

# 2. Search History for '대흥당'
print("\nSearching history for '대흥당'...")
for fp in glob.glob('*.py') + glob.glob('*.json') + glob.glob('*.bak') + glob.glob('scripts/*.py'):
    try:
        with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
            if "대흥당" in f.read():
                print(f"Found '대흥당' in {fp}")
    except: pass

# 3. Analyze Missing 4+ Wins
print("\nAnalyzing shops with 4+ Wins missing POV...")
missing_4wins = []
for s in data:
    wins = s.get('wins', 0)
    try: wins = int(wins)
    except: wins = 0
    
    if wins >= 4:
        # Check POV
        if not s.get('pov') or not s.get('panoid'):
            missing_4wins.append(s)

print(f"Total Shops with 4+ Wins: {len([s for s in data if int(s.get('wins',0) or 0) >= 4])}")
print(f"Missing POV (4+ Wins): {len(missing_4wins)}")
if missing_4wins:
    print("List of missing 4+ wins shops:")
    for s in missing_4wins:
        print(f"  - {s['n']} (Wins: {s.get('wins')}) {s['a']}")
