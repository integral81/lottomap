import pandas as pd
import re

def normalize_address(addr):
    if not isinstance(addr, str):
        return addr
    
    # 1. Basic cleaning
    original = addr
    addr = addr.strip()
    
    # 2. Remove "번지" (beonji)
    # Examples: "19-1번지" -> "19-1", "123번지" -> "123"
    addr = re.sub(r'(\d+)번지', r'\1', addr)
    addr = re.sub(r'(\d+-\d+)번지', r'\1', addr)
    
    # 3. Remove floor/room information for unification (if it follows a number)
    # Examples: "19-1 1층" -> "19-1", "123 1층" -> "123"
    # Many records vary by having " 1층" or not.
    addr = re.sub(r'\s(\d+)층$', '', addr)
    addr = re.sub(r'\s지하\s*(\d*)층?$', '', addr)
    
    # 4. Remove trailing dots or commas
    addr = addr.rstrip('., ')
    
    # Optional: If address ends with "번지" without numbers (rare)
    if addr.endswith('번지'):
        addr = addr[:-2].strip()
        
    return addr

def main():
    file_path = 'temp_data.xlsx'
    print(f"Reading {file_path}...")
    df = pd.read_excel(file_path)
    
    addr_col = df.columns[4] # '소재지' column (5th)
    print(f"Normalizing column: {addr_col}")
    
    # Track changes
    unique_before = df[addr_col].nunique()
    df[addr_col] = df[addr_col].apply(normalize_address)
    unique_after = df[addr_col].nunique()
    
    print(f"Unique addresses: {unique_before} -> {unique_after} ({unique_before - unique_after} unified)")
    
    # Save back
    print("Saving normalized data...")
    df.to_excel(file_path, index=False)
    print("Done!")

if __name__ == "__main__":
    main()
