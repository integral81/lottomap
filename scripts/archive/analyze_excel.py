
import pandas as pd
from collections import defaultdict
import json

def analyze_excel_variations():
    print("--- [ANALYSIS] Finding Variations in Excel ---")
    try:
        df = pd.read_excel('lotto_results_kinov.xlsx')
        
        # Filter rows where 소재지 (Address) is present
        df = df[df['소재지'].notna()]
        
        addr_map = defaultdict(lambda: defaultdict(list))
        
        for idx, row in df.iterrows():
            addr = str(row['소재지']).strip()
            name = str(row['상호명']).strip()
            round_num = row['회차']
            addr_map[addr][name].append(round_num)
            
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
        
        variations.sort(key=lambda x: x['total_wins'], reverse=True)
        
        with open('excel_priority_cases.json', 'w', encoding='utf-8') as f:
            json.dump(variations, f, indent=2, ensure_ascii=False)
            
        print(f"Found {len(variations)} addresses with name variations in Excel.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze_excel_variations()
