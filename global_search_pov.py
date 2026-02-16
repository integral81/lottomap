
import subprocess
import re
import json

def global_search_pov():
    print("Starting Global Git Search for 'panoId'...")
    
    # 1. Get all commit hashes
    try:
        raw_hashes = subprocess.check_output(["git", "rev-list", "--all"])
        commits = raw_hashes.decode('utf-8').splitlines()
        print(f"Scanning {len(commits)} commits...")
    except Exception as e:
        print(f"Error getting commits: {e}")
        return

    unique_povs = {}
    
    # 2. Iterate (Scan chunks or recent 100 deep?)
    # Scanning ALL might be slow. Let's do recent 200 first.
    scan_limit = 200
    count = 0
    
    for commit in commits[:scan_limit]:
        count += 1
        if count % 20 == 0: print(f"  Scanned {count}/{scan_limit}...")
        
        try:
            # Get diff/show content
            # using 'git show' might be huge. 'git grep' is better but harder to context.
            # Let's use git show but limit to lotto_data.json changes?
            # actually user said "270 unregistered lists". Maybe they were in a diff.
            
            raw_show = subprocess.check_output(["git", "show", commit], stderr=subprocess.DEVNULL)
            
            # Decode safely
            try: content = raw_show.decode('utf-8')
            except: content = raw_show.decode('utf-8', errors='ignore')
            
            # Find all "panoId": ... or "id": ... inside "pov" block?
            # Regex for "panoId": 12345
            matches = re.findall(r'["\']?panoId["\']?\s*[:=]\s*["\']?(\d+)["\']?', content)
            
            # Also "id": 12345  (riskier, catch common ones)
            # Context: "pov": { "id": 111 }
            # Let's stick to 'panoId' or large numbers near 'pov'
            
            for pid in matches:
                # Store origin commit
                if pid not in unique_povs:
                    unique_povs[pid] = commit
                    
        except:
            pass
            
    print(f"\nFound {len(unique_povs)} unique PanoIDs in history.")
    
    # Compare with current local file
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        local_data = json.load(f)
        
    local_ids = set()
    for item in local_data:
        pov = item.get('pov')
        if pov:
            pid = str(pov.get('id') or pov.get('panoId'))
            local_ids.add(pid)
            
    print(f"Current Local PanoIDs: {len(local_ids)}")
    
    # Identify Recoverable
    recoverable = []
    for pid, commit in unique_povs.items():
        if pid not in local_ids:
            recoverable.append(pid)
            
    print(f"Recoverable (Lost) PanoIDs: {len(recoverable)}")
    print(f"Recoverable IDs: {recoverable[:20]}...")

if __name__ == "__main__":
    global_search_pov()
