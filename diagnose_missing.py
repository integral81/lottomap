
import pandas as pd
import json

def find_missing_winners(round_num):
    print(f"--- [DIAGNOSIS] Missing Winners in Round {round_num} ---")
    try:
        df_excel = pd.read_excel('lotto_results_kinov.xlsx')
        excel_winners = df_excel[df_excel['회차'] == round_num].copy()
        excel_winners['matched'] = False
        
        with open('lotto_data.json', 'r', encoding='utf-8') as f:
            data_json = json.load(f)
        json_winners = [item for item in data_json if item['r'] == round_num]
        
        for item in json_winners:
            json_name = item['n'].strip()
            # Try to find a match in Excel based on name or partial name
            found = False
            for idx, row in excel_winners.iterrows():
                if row['matched']: continue
                excel_name = str(row['상호명']).strip()
                if excel_name == json_name or excel_name in json_name or json_name in excel_name:
                    excel_winners.at[idx, 'matched'] = True
                    found = True
                    break
        
        missing = excel_winners[excel_winners['matched'] == False]
        print(f"Missing {len(missing)} winners from Excel in JSON:")
        for _, row in missing.iterrows():
            print(f"  - {row['상호명']} | {row['소재지']}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    find_missing_winners(1184)
