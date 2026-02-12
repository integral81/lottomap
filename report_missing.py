
import pandas as pd
import json

def report_missing_winners():
    print("--- [ANALYSIS] Generating Full Missing Winners Report ---")
    try:
        df_excel = pd.read_excel('lotto_results_kinov.xlsx')
        with open('lotto_data.json', 'r', encoding='utf-8') as f:
            data_json = json.load(f)
            
        # Group JSON by round
        json_map = {}
        for item in data_json:
            r = item['r']
            if r not in json_map:
                json_map[r] = []
            json_map[r].append(item)
            
        missing_report = []
        
        for idx, row in df_excel.iterrows():
            r = int(row['회차'])
            excel_name = str(row['상호명']).strip()
            excel_addr = str(row['소재지']).strip()
            
            if r not in json_map:
                missing_report.append({"r": r, "n": excel_name, "a": excel_addr, "reason": "Round Missing"})
                continue
                
            # Try to find a match in the JSON winners for this round
            found = False
            for j_item in json_map[r]:
                j_name = j_item['n'].strip()
                j_addr = j_item['a'].strip()
                
                # Loose matching: Name or Address overlap
                if (excel_name in j_name or j_name in excel_name) and (excel_addr[:10] in j_addr or j_addr[:10] in excel_addr):
                    found = True
                    break
            
            if not found:
                missing_report.append({"r": r, "n": excel_name, "a": excel_addr, "reason": "Winner Missing"})
        
        print(f"Total missing entries identified: {len(missing_report)}")
        
        with open('missing_winners_report.json', 'w', encoding='utf-8') as f:
            json.dump(missing_report, f, indent=2, ensure_ascii=False)
            
        # Summary by round
        from collections import Counter
        rounds = [item['r'] for item in missing_report]
        round_counts = Counter(rounds)
        print("\nTop rounds with missing winners:")
        for r, count in round_counts.most_common(10):
            print(f"  Round {r}: {count} missing")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    report_missing_winners()
