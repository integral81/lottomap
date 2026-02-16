
import json

def analyze_bus_shop():
    """Analyze 버스표판매소 data comprehensively"""
    
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Find all entries
    entries = [item for item in data if "버스표판매소" in item['n']]
    
    if not entries:
        print("No entries found")
        return
    
    # Group by address
    from collections import defaultdict
    by_addr = defaultdict(list)
    
    for entry in entries:
        by_addr[entry['a']].append(entry)
    
    print(f"Found {len(entries)} total entries")
    print(f"Unique addresses: {len(by_addr)}\n")
    
    for addr, items in by_addr.items():
        print(f"Address: {addr}")
        print(f"  Total wins: {len(items)}")
        
        # Get rounds
        rounds = sorted([item['r'] for item in items])
        print(f"  Rounds: {rounds[:3]}...{rounds[-3:] if len(rounds) > 3 else ''}")
        print(f"  Latest round: {max(rounds)}")
        
        # Check coordinates
        coords = [(item.get('lat'), item.get('lng')) for item in items if item.get('lat')]
        if coords:
            print(f"  Coordinates: {coords[0]}")
        
        # Check POV
        has_pov = any(item.get('pov') for item in items)
        print(f"  Has POV: {has_pov}")
        print()

if __name__ == "__main__":
    analyze_bus_shop()
