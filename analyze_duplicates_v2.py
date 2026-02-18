
import json
import math
import sys

# Ensure UTF-8 output
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371000 # Meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def analyze():
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 1. Group records by name
    by_name = {}
    for item in data:
        n = item['n']
        if n not in by_name: by_name[n] = []
        by_name[n].append(item)
    
    report = []
    
    for name, records in by_name.items():
        if len(records) < 2: continue
        
        # Cluster within the same name by distance
        clusters = []
        for r in records:
            r_pos = (float(r.get('lat',0)), float(r.get('lng',0)))
            found = False
            for c in clusters:
                ref_pos = (float(c[0].get('lat',0)), float(c[0].get('lng',0)))
                if calculate_distance(r_pos[0], r_pos[1], ref_pos[0], ref_pos[1]) < 100:
                    c.append(r)
                    found = True
                    break
            if not found: clusters.append([r])
        
        # If we have multiple records in ONE cluster, they are candidates for merging.
        # Especially if their addresses are slightly different.
        for c in clusters:
            if len(c) > 1:
                addrs = list(set(r.get('a') for r in c))
                rounds = sorted([r.get('r') for r in c])
                report.append({
                    "name": name,
                    "addrs": addrs,
                    "rounds": rounds,
                    "coords": (c[0]['lat'], c[0]['lng'])
                })
    
    # Sort by name
    report.sort(key=lambda x: x['name'])
    return report

candidates = analyze()
print(f"TOTAL_CANDIDATES: {len(candidates)}")
# Save as JSON for machine reading next step
with open('merge_candidates.json', 'w', encoding='utf-8') as f:
    json.dump(candidates, f, ensure_ascii=False, indent=2)

# Print first 10 for user review
for i, c in enumerate(candidates[:10], 1):
    print(f"[{i}] 매장명: {c['name']}")
    print(f"    - 당첨회차: {c['rounds']}")
    print(f"    - 등록된 주소들: {c['addrs']}")
    print("-" * 30)
