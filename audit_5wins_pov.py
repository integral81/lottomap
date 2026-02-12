
import json
from collections import Counter

def audit_5wins_pov():
    print("--- [AUDIT] 5+ Wins POV Registration Check ---")
    try:
        # Load Lotto Data
        with open('lotto_data.json', 'r', encoding='utf-8') as f:
            lotto_data = json.load(f)
            
        # Load Verification Data
        try:
            with open('double_check_results.json', 'r', encoding='utf-8') as f:
                verified_data = json.load(f)
        except:
            verified_data = []
            
        verified_addrs = set([item['target_shop_address'].strip() for item in verified_data])
        
        # Aggregate wins
        addr_map = {}
        for item in lotto_data:
            addr = item.get('a', '').strip()
            name = item.get('n', '').strip()
            if not addr: continue
            
            if addr not in addr_map:
                addr_map[addr] = {"name": name, "wins": 0, "has_coords": False}
            
            addr_map[addr]["wins"] += 1
            if item.get('lat') and item.get('lng'):
                addr_map[addr]["has_coords"] = True
        
        # Filter 5+ wins target
        top_shops = {addr: info for addr, info in addr_map.items() if info['wins'] >= 5}
        
        missing_verification = []
        missing_coords = []
        
        for addr, info in top_shops.items():
            # Check if verified (loose match because of address formatting)
            matched = False
            for v_addr in verified_addrs:
                if addr in v_addr or v_addr in addr:
                    matched = True
                    break
            
            if not matched:
                missing_verification.append({"n": info['name'], "a": addr, "w": info['wins']})
            
            if not info['has_coords']:
                missing_coords.append({"n": info['name'], "a": addr, "w": info['wins']})
                
        print(f"Total shops with 5+ wins: {len(top_shops)}")
        print(f"Shops missing from double_check_results.json: {len(missing_verification)}")
        print(f"Shops missing coordinates: {len(missing_coords)}")
        
        results = {
            "missing_verification": sorted(missing_verification, key=lambda x: x['w'], reverse=True),
            "missing_coords": sorted(missing_coords, key=lambda x: x['w'], reverse=True)
        }
        
        with open('audit_5wins_summary.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
            
        print("\nResults saved to audit_5wins_summary.json")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    audit_5wins_pov()
