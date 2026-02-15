
import pandas as pd
import json

def investigate_round(round_num):
    print(f"--- [INVESTIGATION] Round {round_num} ---")
    try:
        df_excel = pd.read_excel('lotto_results_kinov.xlsx')
        excel_winners = df_excel[df_excel['회차'] == round_num]
        
        with open('lotto_data.json', 'r', encoding='utf-8') as f:
            data_json = json.load(f)
        json_winners = [item for item in data_json if item['r'] == round_num]
        
        print(f"Excel count: {len(excel_winners)}")
        print(f"JSON count: {len(json_winners)}")
        
        print("\n[Excel Wins]")
        for _, row in excel_winners.iterrows():
            print(f"  {row['상호명']} | {row['소재지']}")
            
        print("\n[JSON Wins]")
        for item in json_winners:
            print(f"  {item['n']} | {item['a']}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    investigate_round(1184)
