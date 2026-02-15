import pandas as pd

def update_excel_address():
    file_path = 'lotto_results_kinov.xlsx'
    target_name = "송내매표소"
    new_addr = "경기 부천시 소사구 송내1동 709-2"
    
    try:
        df = pd.read_excel(file_path)
        
        # Update address for matching shop name
        mask = df['상호명'].str.contains(target_name, na=False)
        old_addrs = df.loc[mask, '소재지'].unique()
        print(f"Found shop matching '{target_name}'. Old addresses: {old_addrs}")
        
        df.loc[mask, '소재지'] = new_addr
        
        df.to_excel(file_path, index=False)
        print(f"Successfully updated Excel address for {target_name} to {new_addr}.")
        
    except Exception as e:
        print(f"Error updating Excel: {e}")

if __name__ == "__main__":
    update_excel_address()
