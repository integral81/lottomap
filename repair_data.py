import pandas as pd
import ftfy

def repair_text(text):
    if not isinstance(text, str): return text
    # 1. Try common mojibake fix (Latin1 -> CP949)
    try:
        decoded = text.encode('latin1').decode('cp949')
        return decoded
    except:
        pass
    
    # 2. Use ftfy to fix other encoding glitches
    return ftfy.fix_text(text)

try:
    print("Loading corrupted file...")
    df = pd.read_excel('lotto_results_kinov.xlsx')
    
    print("Repairing columns...")
    df.columns = ['회차', '등위', '상호명', '당첨방식', '소재지'] # Force correct headers
    
    print("Repairing data...")
    for col in ['상호명', '당첨방식', '소재지']:
        df[col] = df[col].apply(repair_text)
        
    print("Preview of repaired data:")
    print(df.head())
    
    output_file = 'lotto_results_kinov_repaired.xlsx'
    df.to_excel(output_file, index=False)
    print(f"Saved repaired data to {output_file}")
    
except Exception as e:
    print(f"Repair failed: {e}")
