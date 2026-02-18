import json
import glob

keyword = "온천장"
target_files = [
    'lotto_data.json',
    'lotto_data_clean.json',
    'lotto_data_old.json',
    'lotto_data.current.bak',
    'lotto_data.json.bak'
] + glob.glob('lotto_data_backup*.json')

print(f"Searching for '{keyword}' in backups...")

best_candidate = None

for fname in target_files:
    try:
        with open(fname, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        count = 0
        found_pov = False
        for s in data:
            if keyword in s.get('n', '') or keyword in s.get('a', ''):
                count += 1
                if s.get('pov'):
                    print(f"  [{fname}] Found: {s['n']} (Wins: {s.get('wins')}) has POV!")
                    found_pov = True
                    if not best_candidate:
                        best_candidate = s
        
        if count > 0 and not found_pov:
             print(f"  [{fname}] Found {count} matches but NO POV.")
             
    except Exception as e:
        # print(f"  [{fname}] Error: {e}")
        pass

if best_candidate:
    print("\nBest candidate found!")
    print(json.dumps(best_candidate, ensure_ascii=False, indent=2))
else:
    print("\nNo POV found in any backup.")
