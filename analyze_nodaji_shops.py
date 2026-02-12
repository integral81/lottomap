import json
import math

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points in km"""
    R = 6371  # Earth radius in km
    
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c

def analyze_nodaji_shops():
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Shop 1: 마평동 735-1
    shop1_addr = "경기 용인시 처인구 마평동 735-1"
    shop1_wins = []
    shop1_coords = None
    
    # Shop 2: 금령로 130
    shop2_addr = "경기 용인시 처인구 금령로 130"
    shop2_wins = []
    shop2_coords = None
    
    for entry in data:
        if entry.get('a') == shop1_addr:
            shop1_wins.append({
                'round': entry.get('r'),
                'method': entry.get('m')
            })
            if not shop1_coords:
                shop1_coords = (entry.get('lat'), entry.get('lng'))
        
        elif entry.get('a') == shop2_addr:
            shop2_wins.append({
                'round': entry.get('r'),
                'method': entry.get('m')
            })
            if not shop2_coords:
                shop2_coords = (entry.get('lat'), entry.get('lng'))
    
    # Calculate distance
    if shop1_coords and shop2_coords:
        distance = haversine_distance(
            shop1_coords[0], shop1_coords[1],
            shop2_coords[0], shop2_coords[1]
        )
    else:
        distance = None
    
    # Sort by round
    shop1_wins.sort(key=lambda x: x['round'])
    shop2_wins.sort(key=lambda x: x['round'])
    
    result = {
        'shop1': {
            'address': shop1_addr,
            'coords': shop1_coords,
            'wins': shop1_wins,
            'total_wins': len(shop1_wins)
        },
        'shop2': {
            'address': shop2_addr,
            'coords': shop2_coords,
            'wins': shop2_wins,
            'total_wins': len(shop2_wins)
        },
        'distance_km': round(distance, 2) if distance else None
    }
    
    with open('nodaji_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"Shop 1 (마평동): {len(shop1_wins)} wins")
    print(f"Shop 2 (금령로): {len(shop2_wins)} wins")
    print(f"Distance: {result['distance_km']} km")
    print(f"\nShop 1 rounds: {[w['round'] for w in shop1_wins]}")
    print(f"Shop 2 rounds: {[w['round'] for w in shop2_wins]}")

if __name__ == "__main__":
    analyze_nodaji_shops()
