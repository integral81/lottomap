import json
import glob
import os
import datetime

def find_pov_in_files():
    target_addr_fragment = "156-1" # for Busan Oncheonjang
    target_addr_fragment_2 = "1428" # for Suwan
    
    print(f"Searching for addresses containing '{target_addr_fragment}' or '{target_addr_fragment_2}' with valid POV in ALL json files...")
    
    json_files = glob.glob('*.json') + glob.glob('*.bak')
    
    found_any = False
    
    for filename in json_files:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            if isinstance(data, list):
                count = 0
                for item in data:
                    addr = item.get('a', '')
                    if (target_addr_fragment in addr or target_addr_fragment_2 in addr):
                        if item.get('pov'):
                            print(f"\n[FOUND] File: {filename}")
                            print(f"  Name: {item.get('n')}")
                            print(f"  Addr: {item.get('a')}")
                            print(f"  POV: {item.get('pov')}")
                            found_any = True
            
        except Exception as e:
            # print(f"Skipping {filename}: {e}")
            pass
            
    if not found_any:
        print("\n[FAILURE] No JSON file contains POV data for these specific addresses.")
        print("We must check Python scripts next.")

if __name__ == "__main__":
    find_pov_in_files()
