import pandas as pd

try:
    df = pd.read_excel('lotto_results_kinov.xlsx')
    
    def fix_encoding(text):
        if not isinstance(text, str): return text
        try:
            # Let's try to encode back to original bytes and decode as CP949 or EUC-KR
            # This is a common trick for "mojibake"
            return text.encode('latin1').decode('cp949')
        except:
            return text

    # Try to fix column names
    df.columns = [fix_encoding(c) for c in df.columns]
    print("Fixed Columns:", df.columns.tolist())
    
    # Try to fix some data
    for col in df.columns:
        df[col] = df[col].apply(fix_encoding)
    
    print("Fixed First 5 rows:")
    print(df.head())
    
    # If it works, save it!
    df.to_excel('lotto_results_kinov_fixed.xlsx', index=False)
    print("Saved fixed file to lotto_results_kinov_fixed.xlsx")

except Exception as e:
    print(f"Error: {e}")
