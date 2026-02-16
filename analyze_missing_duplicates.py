
import json
import math
from collections import defaultdict

def haversine_distance(lat1, lng1, lat2, lng2):
    """Calculate distance between two points in meters"""
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lng2 - lng1)
    a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def analyze_missing_duplicates():
    """
    Analyze Missing list (POV 없는 매장) for potential duplicates
    Same name + within 1km = likely same shop, keep only one
    """
    print("Loading admin_targets.js...")
    
    # Read admin_targets.js
    with open('admin_targets.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse JSON (remove "const adminTargets = " and trailing ";")
    json_str = content.replace('const adminTargets = ', '').rstrip(';')
    targets = json.loads(json_str)
    
    # Separate by category
    missing = []
    recovered = []
    
    for target in targets:
        if 'panoId' in target:
            recovered.append(target)
        else:
            missing.append(target)
    
    print(f"\nTotal targets: {len(targets)}")
    print(f"Recovered (POV 있음): {len(recovered)}")
    print(f"Missing (POV 없음): {len(missing)}")
    
    # Group missing by shop name
    missing_groups = defaultdict(list)
    for shop in missing:
        missing_groups[shop['name']].append(shop)
    
    # Find duplicates within 1km
    duplicate_candidates = []
    
    for name, shops in missing_groups.items():
        if len(shops) <= 1:
            continue
        
        # Check distances between all pairs
        for i, shop1 in enumerate(shops):
            for j, shop2 in enumerate(shops):
                if i >= j:
                    continue
                
                lat1 = shop1.get('lat', 0)
                lng1 = shop1.get('lng', 0)
                lat2 = shop2.get('lat', 0)
                lng2 = shop2.get('lng', 0)
                
                if lat1 == 0 or lng1 == 0 or lat2 == 0 or lng2 == 0:
                    continue
                
                distance = haversine_distance(lat1, lng1, lat2, lng2)
                
                if distance <= 1000:  # Within 1km
                    duplicate_candidates.append({
                        'name': name,
                        'shop1': shop1,
                        'shop2': shop2,
                        'distance_m': round(distance, 1)
                    })
    
    # Sort by distance
    duplicate_candidates.sort(key=lambda x: x['distance_m'])
    
    print(f"\n{'='*80}")
    print(f"MISSING LIST DUPLICATES (1km radius)")
    print(f"{'='*80}\n")
    
    total_removable = 0
    for dup in duplicate_candidates[:30]:  # Top 30
        print(f"\n{dup['name']} - {dup['distance_m']}m apart")
        print(f"  1. {dup['shop1']['address']} ({dup['shop1']['wins']} wins)")
        print(f"  2. {dup['shop2']['address']} ({dup['shop2']['wins']} wins)")
        total_removable += 1
    
    print(f"\n{'='*80}")
    print(f"Total duplicate pairs found: {len(duplicate_candidates)}")
    print(f"Potential shops to remove: {len(duplicate_candidates)}")
    print(f"New Missing list size: {len(missing)} → {len(missing) - len(duplicate_candidates)}")
    print(f"{'='*80}\n")
    
    # Save report
    with open('missing_duplicates.json', 'w', encoding='utf-8') as f:
        json.dump(duplicate_candidates, f, ensure_ascii=False, indent=2)
    
    print("Report saved to: missing_duplicates.json")
    
    return duplicate_candidates

if __name__ == "__main__":
    analyze_missing_duplicates()
