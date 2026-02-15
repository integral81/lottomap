import pandas as pd

files = [
    r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_results_kinov.xlsx",
    r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\archive_v5\lotto_raw.xlsx"
]

for file in files:
    print(f"Checking {file}...")
    try:
        df = pd.read_excel(file)
        # Search for address containing "심곡동 302"
        # Column names could be different, usually '상호', '주소' or 'n', 'a'
        # Let's see columns first
        print(f"Columns: {df.columns.tolist()}")
        
        # Search in all columns
        mask = df.apply(lambda row: row.astype(str).str.contains('심곡동 302').any(), axis=1)
        matches = df[mask]
        
        if not matches.empty:
            print(f"Found {len(matches)} matches:")
            print(matches.to_string())
        else:
            print("No matches found.")
    except Exception as e:
        print(f"Error: {e}")
    print("-" * 20)
