
import json
import math

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371000 # Meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def analyze_duplicates():
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 1. Group records by unique "Record Identity" to see current unique entries
    # Actually, let's group by name and see their spread
    shops_by_name = {}
    for item in data:
        name = item['n']
        if name not in shops_by_name:
            shops_by_name[name] = []
        shops_by_name[name].append(item)
    
    potential_merges = [] # Same name, slightly different info
    ambiguous_cases = [] # High risk cases
    
    for name, records in shops_by_name.items():
        if len(records) < 2: continue
        
        # Check coordinates and addresses within the same name
        sub_groups = [] # Each sub-group is a potential unique shop
        for r in records:
            matched = False
            r_lat, r_lng = float(r.get('lat', 0)), float(r.get('lng', 0))
            
            for group in sub_groups:
                ref = group[0]
                ref_lat, ref_lng = float(ref.get('lat', 0)), float(ref.get('lng', 0))
                
                dist = calculate_distance(r_lat, r_lng, ref_lat, ref_lng)
                # If name is same and distance < 50m, likely same shop but coords slightly off or addr format diff
                if dist < 50:
                    group.append(r)
                    matched = True
                    break
            
            if not matched:
                sub_groups.append([r])
        
        if len(sub_groups) > 1:
            # Same name but separate locations found!
            ambiguous_cases.append({
                "type": "Same Name / Different Location",
                "name": name,
                "locations": sub_groups
            })
        elif len(sub_groups) == 1 and len(records) > 1:
            # Same name, same location, but multiple records
            # Check if addresses or other fields vary
            addrs = {r.get('a') for r in records}
            if len(addrs) > 1:
                potential_merges.append({
                    "type": "Same Shop / Different Address Strings",
                    "name": name,
                    "addresses": list(addrs),
                    "count": len(records)
                })

    # Let's also check for different names but same coordinates
    # (Omitted mapping for brevity in first report, focusing on Name-based first)
    
    return potential_merges, ambiguous_cases

p_merges, a_cases = analyze_duplicates()
print(f"--- Analysis Result ---")
print(f"Definite Duplicates (to merge): {len(p_merges)}")
print(f"Ambiguous Cases (need review): {len(a_cases)}")
print("\n[Preview: Potential Merges - Same Shop, Diff Addr Format]")
for m in p_merges[:5]:
    print(f"- {m['name']}: {m['addresses']}")

print("\n[Preview: Ambiguous - Same Name, Diff Places]")
for c in a_cases[:3]:
    print(f"- {c['name']} has {len(c['locations'])} distinct locations.")
