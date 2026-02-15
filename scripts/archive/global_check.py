
import pandas as pd
import json

def global_sync_check():
    print("--- [ANALYSIS] Global Sync Check: Excel vs JSON ---")
    try:
        # Load Excel Ground Truth
        df_excel = pd.read_excel('lotto_results_kinov.xlsx')
        excel_data = {}
        for _, row in df_excel.iterrows():
            r = int(row['회차'])
            name = str(row['상호명']).strip()
            addr = str(row['소재지']).strip()
            if r not in excel_data:
                excel_data[r] = []
            excel_data[r].append({"n": name, "a": addr})
            
        # Load JSON
        with open('lotto_data.json', 'r', encoding='utf-8') as f:
            data_json = json.load(f)
            
        json_data = {}
        for item in data_json:
            r = item['r']
            if r not in json_data:
                json_data[r] = []
            json_data[r].append(item)
            
        discrepancies = []
        
        # Check all rounds in Excel
        for r, excel_winners in excel_data.items():
            if r not in json_data:
                discrepancies.append(f"Round {r}: Missing entirely in JSON")
                continue
                
            json_winners = json_data[r]
            
            # Simple count check
            if len(excel_winners) != len(json_winners):
                # Only log if it's a significant mismatch (sometimes we intentionally consolidate, 
                # but for 100% accuracy we want to know why)
                discrepancies.append(f"Round {r}: Count mismatch (Excel: {len(excel_winners)}, JSON: {len(json_winners)})")
        
        # Total rounds check
        print(f"Excel rounds: {len(excel_data)}")
        print(f"JSON rounds: {len(json_data)}")
        
        if discrepancies:
            print(f"Found {len(discrepancies)} count/presence discrepancies.")
            for d in discrepancies[:20]: # Show first 20
                print(f"  {d}")
        else:
            print("No count/presence discrepancies found.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    global_sync_check()
