import pandas as pd
import re

def normalize_address(addr):
    if not isinstance(addr, str):
        return addr
    
    # Same rules as normalize_addresses.py
    addr = addr.strip()
    addr = re.sub(r'(\d+)번지', r'\1', addr)
    addr = re.sub(r'(\d+-\d+)번지', r'\1', addr)
    addr = re.sub(r'\s(\d+)층$', '', addr)
    addr = re.sub(r'\s지하\s*(\d*)층?$', '', addr)
    addr = addr.rstrip('., ')
    if addr.endswith('번지'):
        addr = addr[:-2].strip()
        
    return addr

def main():
    file_path = 'geocoded_cache_healthy.xlsx'
    print(f"Normalizing cache: {file_path}")
    df = pd.read_excel(file_path)
    
    # Column 'a' is address in cache
    df['a'] = df['a'].apply(normalize_address)
    
    # Remove duplicates in cache after normalization (keep first)
    df = df.drop_duplicates(subset=['a'])
    
    df.to_excel(file_path, index=False)
    print(f"Cache updated. Unique entries: {len(df)}")

if __name__ == "__main__":
    main()
