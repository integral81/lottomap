
import json
from collections import Counter

def list_null_coords():
    print("--- [ANALYSIS] Listing Null Coordinate Addresses ---")
    try:
        with open('lotto_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        null_items = [item for item in data if not item.get('lat')]
        print(f"Total entries with null coordinates: {len(null_items)}")
        
        # De-duplicate by address
        addr_counts = Counter([item['a'] for item in null_items])
        unique_addrs = list(addr_counts.keys())
        print(f"Unique addresses to geocode: {len(unique_addrs)}")
        
        # Save to a temporary file for processing
        with open('addrs_to_geocode.json', 'w', encoding='utf-8') as f:
            json.dump(unique_addrs, f, indent=2, ensure_ascii=False)
            
        # Preview top 10
        print("\nPreview of addresses needing geocoding:")
        for addr in unique_addrs[:10]:
            print(f"  - {addr} ({addr_counts[addr]} wins)")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_null_coords()
