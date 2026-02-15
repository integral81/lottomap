import pandas as pd

files = [
    r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_results_kinov.xlsx",
    r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\archive_v5\lotto_raw.xlsx"
]

search_terms = ["보람복권방", "삼산동 1567-6", "화합로194번길"]

for file in files:
    print(f"Checking {file}...")
    try:
        try:
            df = pd.read_excel(file)
        except:
            df = pd.read_excel(file, engine='openpyxl')
            
        print(f"Columns: {df.columns.tolist()}")
        
        results = []
        for term in search_terms:
            mask = df.apply(lambda row: row.astype(str).str.contains(term, case=False).any(), axis=1)
            matches = df[mask]
            if not matches.empty:
                results.append(matches)
        
        if results:
            final_matches = pd.concat(results).drop_duplicates()
            print(f"Found {len(final_matches)} matches:")
            print(final_matches.to_string())
        else:
            print("No matches found.")
    except Exception as e:
        print(f"Error checking {file}: {e}")
    print("-" * 30)
