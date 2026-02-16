
import subprocess
import re
import json

def map_recovered_ids():
    # IDs found by previous step (hardcoded or re-scan?)
    # Re-running the scan is safer to get context.
    
    print("Mapping Recovered PanoIDs to Shop Names...")
    
    # 1. Get all commits (limit 200)
    raw_hashes = subprocess.check_output(["git", "rev-list", "--all"])
    commits = raw_hashes.decode('utf-8').splitlines()[:200]
    
    recovered_map = {} # pid -> {name, addr, etc}
    
    for i, commit in enumerate(commits):
        if i % 50 == 0: print(f"  Scanning commit {i}...")
        try:
            raw = subprocess.check_output(["git", "show", commit], stderr=subprocess.DEVNULL)
            try: content = raw.decode('utf-8')
            except: content = raw.decode('utf-8', errors='ignore')
            
            # Find blocks with "panoId"
            # Regex to capture context: { ... "name": "...", ... "panoId": 123 ... }
            # Since JSON formatting varies, let's look for "panoId": 123 and then search backwards for "name"
            
            pids = re.finditer(r'["\']?panoId["\']?\s*[:=]\s*["\']?(\d+)["\']?', content)
            
            for m in pids:
                pid = m.group(1)
                
                # Context Search
                start = max(0, m.start() - 500)
                end = min(len(content), m.end() + 200)
                snippet = content[start:end]
                
                # Find Name
                name_match = re.search(r'["\']?n["\']?\s*[:=]\s*["\']([^"\']+)["\']', snippet) # 'n': "ShopName"
                if not name_match:
                    name_match = re.search(r'["\']?name["\']?\s*[:=]\s*["\']([^"\']+)["\']', snippet)
                    
                name = name_match.group(1) if name_match else "Unknown"
                
                # Find Addr
                addr_match = re.search(r'["\']?a["\']?\s*[:=]\s*["\']([^"\']+)["\']', snippet)
                addr = addr_match.group(1) if addr_match else ""
                
                if pid not in recovered_map and name != "Unknown":
                    recovered_map[pid] = {"name": name, "addr": addr, "commit": commit[:7]}
                    
        except:
            pass
            
    # Filter against current local
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        local = json.load(f)
    local_ids = set()
    for item in local:
        pov = item.get('pov')
        if pov:
            local_ids.add(str(pov.get('id') or pov.get('panoId')))
            
    final_recovered = []
    for pid, info in recovered_map.items():
        if pid not in local_ids:
            # We found a lost one!
            info['panoId'] = pid
            final_recovered.append(info)
            
    print(f"\nFinal Unique Recovered: {len(final_recovered)}")
    
    # Save to file
    with open('recovered_list_mapped.json', 'w', encoding='utf-8') as f:
        json.dump(final_recovered, f, indent=2, ensure_ascii=False)
        
    # Check if targets are in there
    targets = [
        "황금복권방", "복권명당", "가판점", "GS25", "목화휴게소", 
        "cu", "복권판매점", "뉴빅마트", "대박찬스", "로또휴게실"
    ]
    print("\nTarget Check:")
    for t in targets:
        found = next((r for r in final_recovered if t in r['name']), None)
        if found:
            print(f"  [RECOVERED] {t} -> {found['name']} ({found['panoId']})")
        else:
            print(f"  [MISSING] {t}")

if __name__ == "__main__":
    map_recovered_ids()
