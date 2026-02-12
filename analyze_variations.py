
import json
from collections import defaultdict

def analyze_all_variations():
    print("--- [ANALYSIS] Finding All Name Variations ---")
    try:
        with open('lotto_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        addr_map = defaultdict(lambda: defaultdict(list))
        
        for item in data:
            addr = item.get('a', '').strip()
            name = item.get('n', '').strip()
            round_num = item.get('r')
            if addr and name:
                addr_map[addr][name].append(round_num)
                
        # Filter for addresses with 2+ different names
        variations = []
        for addr, names in addr_map.items():
            if len(names) > 1:
                total_wins = sum(len(rounds) for rounds in names.values())
                var_list = []
                for name, rounds in names.items():
                    var_list.append({"name": name, "rounds": sorted(rounds)})
                
                variations.append({
                    "address": addr,
                    "total_wins": total_wins,
                    "variations": var_list
                })
        
        # Sort by total wins descending
        variations.sort(key=lambda x: x['total_wins'], reverse=True)
        
        with open('full_priority_cases.json', 'w', encoding='utf-8') as f:
            json.dump(variations, f, indent=2, ensure_ascii=False)
            
        print(f"Found {len(variations)} addresses with name variations.")
        print(f"Results saved to full_priority_cases.json")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze_all_variations()
