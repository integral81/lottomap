
import json
from collections import defaultdict
from difflib import SequenceMatcher

def similar(a, b):
    """Calculate similarity ratio between two strings"""
    return SequenceMatcher(None, a, b).ratio()

def analyze_duplicates():
    """Deep analysis to find duplicate/scattered shop records"""
    print("Loading lotto_data.json...")
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Total records: {len(data)}")
    
    # Group by shop name
    shop_groups = defaultdict(list)
    for item in data:
        name = item['n']
        shop_groups[name].append(item)
    
    print(f"\nTotal unique shop names: {len(shop_groups)}")
    
    # Find shops with POV that still appear multiple times
    pov_shops_with_multiple_records = []
    
    for name, records in shop_groups.items():
        # Check if any record has POV
        has_pov = any(r.get('pov') and r['pov'].get('id') != 'N/A' for r in records)
        
        if has_pov:
            # Group by address to see if there are variations
            addr_groups = defaultdict(list)
            for r in records:
                addr_groups[r['a']].append(r)
            
            if len(addr_groups) > 1:
                # Multiple addresses for same shop name with POV
                pov_shops_with_multiple_records.append({
                    'name': name,
                    'addresses': list(addr_groups.keys()),
                    'total_records': len(records),
                    'address_count': len(addr_groups)
                })
    
    print(f"\n{'='*80}")
    print(f"CRITICAL: Shops with POV but scattered across multiple addresses:")
    print(f"{'='*80}")
    
    for shop in sorted(pov_shops_with_multiple_records, key=lambda x: x['total_records'], reverse=True):
        print(f"\n{shop['name']} - {shop['total_records']} records across {shop['address_count']} addresses:")
        for addr in shop['addresses']:
            print(f"  - {addr}")
    
    # Find similar shop names (potential duplicates with typos or variations)
    print(f"\n{'='*80}")
    print(f"Analyzing similar shop names (potential duplicates)...")
    print(f"{'='*80}")
    
    shop_names = list(shop_groups.keys())
    similar_pairs = []
    
    for i, name1 in enumerate(shop_names):
        for name2 in shop_names[i+1:]:
            similarity = similar(name1, name2)
            if 0.7 < similarity < 1.0:  # Similar but not identical
                similar_pairs.append({
                    'name1': name1,
                    'name2': name2,
                    'similarity': similarity,
                    'records1': len(shop_groups[name1]),
                    'records2': len(shop_groups[name2])
                })
    
    for pair in sorted(similar_pairs, key=lambda x: x['similarity'], reverse=True)[:20]:
        print(f"\n{pair['similarity']:.2%} similar:")
        print(f"  1. {pair['name1']} ({pair['records1']} records)")
        print(f"  2. {pair['name2']} ({pair['records2']} records)")
    
    # Save detailed report
    report = {
        'pov_shops_with_multiple_addresses': pov_shops_with_multiple_records,
        'similar_name_pairs': similar_pairs[:50]
    }
    
    with open('duplicate_analysis_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*80}")
    print(f"Report saved to: duplicate_analysis_report.json")
    print(f"{'='*80}")
    
    return report

if __name__ == "__main__":
    analyze_duplicates()
