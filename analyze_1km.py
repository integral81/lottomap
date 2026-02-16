
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

def analyze_1km_radius():
    """Analyze with 1km radius instead of 500m"""
    print("Loading lotto_data.json...")
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Group by shop name
    shop_groups = defaultdict(list)
    for item in data:
        name = item['n']
        shop_groups[name].append(item)
    
    # Find consolidation candidates (1km radius)
    consolidation_candidates = []
    
    for name, records in shop_groups.items():
        # Stage 1: Check if any record has POV
        pov_records = [r for r in records if r.get('pov') and r['pov'].get('id') != 'N/A']
        
        if not pov_records:
            continue
        
        # Group by address
        addr_groups = defaultdict(list)
        for r in records:
            addr_groups[r['a']].append(r)
        
        if len(addr_groups) <= 1:
            continue
        
        # Stage 2 & 3: Check geographic proximity (1km radius)
        addresses = list(addr_groups.keys())
        proximity_groups = []
        
        for i, addr1 in enumerate(addresses):
            group = {
                'main_address': addr1,
                'main_records': addr_groups[addr1],
                'nearby_addresses': []
            }
            
            lat1 = addr_groups[addr1][0].get('lat', 0)
            lng1 = addr_groups[addr1][0].get('lng', 0)
            
            if lat1 == 0 or lng1 == 0:
                continue
            
            for j, addr2 in enumerate(addresses):
                if i >= j:
                    continue
                
                lat2 = addr_groups[addr2][0].get('lat', 0)
                lng2 = addr_groups[addr2][0].get('lng', 0)
                
                if lat2 == 0 or lng2 == 0:
                    continue
                
                distance = haversine_distance(lat1, lng1, lat2, lng2)
                
                if distance <= 1000:  # Within 1km
                    group['nearby_addresses'].append({
                        'address': addr2,
                        'distance_m': round(distance, 1),
                        'records': addr_groups[addr2]
                    })
            
            if group['nearby_addresses']:
                proximity_groups.append(group)
        
        if proximity_groups:
            consolidation_candidates.append({
                'shop_name': name,
                'total_records': len(records),
                'total_addresses': len(addr_groups),
                'proximity_groups': proximity_groups
            })
    
    consolidation_candidates.sort(key=lambda x: x['total_records'], reverse=True)
    
    # Print report
    print(f"\n{'='*80}")
    print(f"CONSOLIDATION CANDIDATES (1km radius)")
    print(f"{'='*80}\n")
    
    for candidate in consolidation_candidates:
        print(f"\n{candidate['shop_name']} - {candidate['total_records']} records, {candidate['total_addresses']} addresses")
        
        for group in candidate['proximity_groups']:
            print(f"\n  Main: {group['main_address']}")
            print(f"  Records: {len(group['main_records'])}")
            
            for nearby in group['nearby_addresses']:
                print(f"    -> {nearby['address']} ({nearby['distance_m']}m away, {len(nearby['records'])} records)")
    
    # Save report
    with open('consolidation_1km.json', 'w', encoding='utf-8') as f:
        json.dump(consolidation_candidates, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*80}")
    print(f"Total candidates: {len(consolidation_candidates)}")
    print(f"Report saved to: consolidation_1km.json")
    print(f"{'='*80}\n")
    
    return consolidation_candidates

if __name__ == "__main__":
    analyze_1km_radius()
