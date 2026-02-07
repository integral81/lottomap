import pandas as pd
import os

def update_verification():
    verification_file = "lotto_verification_1205_1209_corrected.xlsx"
    final_file = "lotto_historic_numbers_1_1209_Final.xlsx"
    
    if not os.path.exists(verification_file):
        print(f"[ERR] {verification_file} not found.")
        return
    if not os.path.exists(final_file):
        print(f"[ERR] {final_file} not found.")
        return
        
    print(f"[*] Reading {final_file}...")
    df_final = pd.read_excel(final_file)
    
    print(f"[*] Reading {verification_file}...")
    df_ver = pd.read_excel(verification_file)
    
    # Update only rounds present in verification file (1205-1209)
    rounds_to_update = df_ver['회차'].unique()
    
    for r in rounds_to_update:
        if r in df_final['회차'].values:
            source_row = df_final[df_final['회차'] == r].iloc[0]
            # Update values in df_ver
            idx = df_ver[df_ver['회차'] == r].index[0]
            df_ver.at[idx, '번호1'] = source_row['번호1']
            df_ver.at[idx, '번호2'] = source_row['번호2']
            df_ver.at[idx, '번호3'] = source_row['번호3']
            df_ver.at[idx, '번호4'] = source_row['번호4']
            df_ver.at[idx, '번호5'] = source_row['번호5']
            df_ver.at[idx, '번호6'] = source_row['번호6']
            print(f"[OK] Updated Round {r}")
        else:
            print(f"[WARN] Round {r} not found in final data.")
            
    # Save the updated file
    df_ver.to_excel(verification_file, index=False)
    print(f"\n[SUCCESS] Updated {verification_file}")
    print(df_ver.to_string(index=False))

if __name__ == "__main__":
    update_verification()
