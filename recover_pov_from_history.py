import subprocess
import json
import os

# List of commits to harvest POV data from (Newest to Oldest relevant)
# These represent the state of the data as the user was working on it over the last 2 days.
commits = [
    "36d02ea", # Batch 14
    "36fb4a8", # Batch 13
    "f5ea40c", # Batch 12
    "51da928", # Batch 11
    "1f7cd89", # Batch 10
    "ad64b03", # Standardize POV structure
    "9de3ec0", # Okjwa POV
    "fbfb2ea", # Pre-restore state (Might be the one with correct POVs but missing shops?)
    "0ebca5b", # Exclude registered 
    "97eb577"  # Start batch 10
]

target_file = "lotto_data.json"

def get_file_content_at_commit(commit_hash, filepath):
    try:
        # git show <commit>:<file>
        cmd = ["git", "show", f"{commit_hash}:{filepath}"]
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            return result.stdout
        else:
            # Try CP949 if UTF-8 fails? Git usually outputs UTF-8 or raw bytes.
            # Let's hope for UTF-8.
            print(f"Error reading {filepath} at {commit_hash}: {result.stderr}")
            return None
    except Exception as e:
        print(f"Exception reading {filepath} at {commit_hash}: {e}")
        return None

def main():
    # 1. Load CURRENT data (Target to update)
    with open(target_file, 'r', encoding='utf-8') as f:
        current_data = json.load(f)
    
    print(f"Current data has {len(current_data)} records.")
    
    # 2. Build a comprehensive POV map from history
    # Key: Name (stripped) -> POV Data
    # We use a set of keys to robustly match: Name|AddrPrefix
    pov_map = {}
    
    for commit in commits:
        print(f"Harvesting from commit {commit}...")
        content = get_file_content_at_commit(commit, target_file)
        if not content: continue
        
        try:
            data = json.loads(content)
            count = 0
            for s in data:
                if s.get('pov') and s.get('panoid'):
                    # Store by Name
                    n = s.get('n', '').strip()
                    if n:
                        # Prioritize: If we already have this name, maybe the NEWER commit is better?
                        # We are iterating Newest to Oldest. So if we find it, we keep it (or overwrite? No, keep the first one found = newest).
                        if n not in pov_map:
                            pov_map[n] = s
                            count += 1
                        
                        # Also Store by Name+Addr (for duplicates)
                        a = s.get('a', '').split(' ')[0] # City
                        k = f"{n}|{a}"
                        if k not in pov_map:
                            pov_map[k] = s
                            
            print(f"  -> Found {count} new unique POVs.")
        except json.JSONDecodeError:
            print("  -> JSON Decode Error")

    print(f"Total unique POVs harvested: {len(pov_map)}")

    # 3. Apply to Current Data
    restored_count = 0
    
    # Identify targets: Shops with wins >= 3 and NO POV
    for s in current_data:
        wins = s.get('wins', 0)
        try: wins = int(wins)
        except: wins = 0
        
        # We process ALL missing POVs, but prioritize wins>=3 logging
        if not s.get('pov'):
            n = s.get('n', '').strip()
            a = s.get('a', '').split(' ')[0] # City prefix
            
            # Try Match
            candidate = None
            if n in pov_map:
                candidate = pov_map[n]
            elif f"{n}|{a}" in pov_map:
                candidate = pov_map[f"{n}|{a}"]
            
            if candidate:
                s['pov'] = candidate['pov']
                s['panoid'] = candidate['panoid']
                # Sync ID
                if 'id' not in s['pov']:
                    s['pov']['id'] = s['panoid']
                
                restored_count += 1
                if wins >= 3:
                    print(f"Restored High-Win Shop: {n} (Wins: {wins})")

    print(f"Restored {restored_count} POVs in total.")

    # 4. Save
    if restored_count > 0:
        with open(target_file, 'w', encoding='utf-8') as f:
            json.dump(current_data, f, ensure_ascii=False, indent=4)
        with open(target_file.replace('.json', '.js'), 'w', encoding='utf-8') as f:
            f.write('const lottoData = ' + json.dumps(current_data, ensure_ascii=False) + ';')
        print("Detailed restoration complete.")
    else:
        print("No matches found in history.")

if __name__ == "__main__":
    main()
