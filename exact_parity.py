
import pandas as pd
import json

def achieve_exact_parity():
    print("--- [EXECUTION] Achieving Exact Parity with Excel Ground Truth ---")
    try:
        df_excel = pd.read_excel('lotto_results_kinov.xlsx')
        with open('lotto_data.json', 'r', encoding='utf-8') as f:
            data_json = json.load(f)
            
        # Group Excel by round
        excel_map = {}
        for _, row in df_excel.iterrows():
            r = int(row['회차'])
            if r not in excel_map: excel_map[r] = []
            excel_map[r].append({"n": str(row['상호명']).strip(), "a": str(row['소재지']).strip()})
            
        # Group JSON by round
        json_map = {}
        for item in data_json:
            r = item['r']
            if r not in json_map: json_map[r] = []
            json_map[r].append(item)
            
        new_data = []
        
        # Iterate through all rounds (1 to 1209)
        all_rounds = sorted(excel_map.keys(), reverse=True)
        
        for r in all_rounds:
            excel_winners = excel_map[r]
            json_winners = json_map.get(r, [])
            
            final_round_winners = []
            
            # For each excel winner, try to find the BEST match in JSON
            temp_json_winners = list(json_winners)
            
            for e_win in excel_winners:
                best_match_idx = -1
                # Try exact name match first
                for i, j_win in enumerate(temp_json_winners):
                    if j_win['n'] == e_win['n'] and (e_win['a'][:10] in j_win['a'] or j_win['a'][:10] in e_win['a']):
                        best_match_idx = i
                        break
                
                # If no exact name match, try loose name match
                if best_match_idx == -1:
                    for i, j_win in enumerate(temp_json_winners):
                        if (e_win['n'] in j_win['n'] or j_win['n'] in e_win['n']) and (e_win['a'][:10] in j_win['a'] or j_win['a'][:10] in e_win['a']):
                            best_match_idx = i
                            break
                            
                # If still no match, try very loose addr match (for "Legend shops" where rename might have happened)
                if best_match_idx == -1:
                   for i, j_win in enumerate(temp_json_winners):
                        if e_win['a'][:15] == j_win['a'][:15]: # Same address start
                            best_match_idx = i
                            break

                if best_match_idx != -1:
                    # Match found! Preserve JSON metadata (coords) but use Excel name/addr ground truth?
                    # Actually, keeping JSON name/addr is better if we already unified them.
                    # But multiplicity is key.
                    matched_win = temp_json_winners.pop(best_match_idx)
                    final_round_winners.append(matched_win)
                else:
                    # No match! Create new from Excel
                    new_win = {
                        "r": r,
                        "n": e_win['n'],
                        "a": e_win['a'],
                        "m": "알수없음",
                        "lat": None,
                        "lng": None
                    }
                    # Try to steal coords from ANY winner at same address in current round or all data
                    # (Quick check in current round)
                    for already_matched in final_round_winners:
                        if already_matched['a'][:15] == e_win['a'][:15] and already_matched.get('lat'):
                            new_win['lat'], new_win['lng'] = already_matched['lat'], already_matched['lng']
                            break
                    final_round_winners.append(new_win)
            
            new_data.extend(final_round_winners)
            
        print(f"Total winners in new data: {len(new_data)}")
        
        with open('lotto_data.json', 'w', encoding='utf-8') as f:
            json.dump(new_data, f, indent=2, ensure_ascii=False)
            
        print("Success: Final lotto_data.json created with exact parity.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    achieve_exact_parity()
