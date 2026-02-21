
import json
import pandas as pd
import os
import sys
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

JSON_PATH = 'lotto_data.json'
JS_PATH = 'lotto_data.js'
EXCEL_PATH = 'lotto_cutted data final.xlsx'

def clean_addr(a):
    if not isinstance(a, str): return ""
    # Remove all non-alphanumeric/hangul characters and spaces
    a = re.sub(r'[^a-zA-Z0-9가-힣]', '', a)
    # Common variations to ignore
    a = a.replace("가판", "").replace("폐점", "").replace("폐업", "").replace("호", "")
    return a

def clean_name(n):
    if not isinstance(n, str): return ""
    n = re.sub(r'[^a-zA-Z0-9가-힣]', '', n)
    return n

def sync_data():
    if not os.path.exists(JSON_PATH):
        print("Error: lotto_data.json not found.")
        return

    # 1. Load existing geocoded data
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        master_data = json.load(f)
    print(f"Loaded {len(master_data)} shops from JSON.")

    # 2. Load Excel History
    print(f"Loading Excel {EXCEL_PATH}...")
    df_hist = pd.read_excel(EXCEL_PATH)
    
    # Identify columns by looking at content if headers are mangled
    # ['ȸ', '2nd', '÷', '', '3rd', '1st', 'θּ']
    # Round is likely first col
    # Name is 2nd (index 1)
    # Method is 3rd (index 2)
    # Address is index 5 or 6
    
    col_round = df_hist.columns[0]
    col_name = df_hist.columns[1]
    col_method = df_hist.columns[2]
    col_addr1 = df_hist.columns[5] # '1st'
    col_addr2 = df_hist.columns[6] # '도로명주소'

    history_db = {}
    print("Building history database from Excel...")
    
    for _, row in df_hist.iterrows():
        try:
            r = int(row[col_round])
            name = str(row[col_name]).strip()
            addr1 = str(row[col_addr1]).strip() if pd.notnull(row[col_addr1]) else ""
            addr2 = str(row[col_addr2]).strip() if pd.notnull(row[col_addr2]) else ""
            method = str(row[col_method]).strip() if pd.notnull(row[col_method]) else "정보없음"
            
            # Index by normalized addresses and name variations
            keys = [
                (clean_name(name), clean_addr(addr1)),
                (clean_name(name), clean_addr(addr2))
            ]
            
            for key in set(keys):
                if not key[0] or not key[1]: continue
                if key not in history_db:
                    history_db[key] = []
                if not any(item['r'] == r for item in history_db[key]):
                    history_db[key].append({"r": r, "m": method})
        except Exception as e:
            continue

    print(f"Compiled history for {len(history_db)} unique (name, addr) keys.")

    # 3. Update master data
    updated_count = 0
    fail_count = 0
    fail_list = []
    
    for shop in master_data:
        name = clean_name(shop['n'])
        addr = clean_addr(shop['a'])
        
        match_found = False
        
        # Strategy A: Exact normalized (name, addr) match
        if (name, addr) in history_db:
            history = history_db[(name, addr)]
            match_found = True
        else:
            # Strategy B: Address match, and name is similar
            # Iterate through keys to find address match
            for (db_name, db_addr), rounds in history_db.items():
                if db_addr == addr:
                    if name in db_name or db_name in name:
                        history = rounds
                        match_found = True
                        break
        
        if match_found:
            sorted_rounds = sorted(history, key=lambda x: x['r'], reverse=True)
            shop['rounds'] = sorted_rounds
            shop['totalWins'] = len(sorted_rounds)
            shop['w'] = len(sorted_rounds)
            if sorted_rounds:
                shop['r'] = sorted_rounds[0]['r']
            updated_count += 1
        else:
            # Keep existing w but rounds might be placeholders
            if not shop.get('rounds') or shop['rounds'][0].get('m') == "정보없음":
                fail_count += 1
                fail_list.append(f"{shop['n']} | {shop['a']}")

    print(f"Successfully updated: {updated_count} shops.")
    print(f"Failed to find history for: {fail_count} shops.")
    
    if fail_list:
        print("\n--- Top 5 Fails Sample ---")
        for f in fail_list[:5]:
            print(f)

    # 4. Save
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(master_data, f, ensure_ascii=False, indent=4)
    
    js_content = f"const lottoData = {json.dumps(master_data, ensure_ascii=False, indent=4)};"
    with open(JS_PATH, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print(f"\nFinal sync complete. Saved to {JSON_PATH} and {JS_PATH}")

if __name__ == "__main__":
    sync_data()
