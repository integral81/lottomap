
import json

def inspect_pov_status():
    print("--- Inspecting POV Status ---")
    
    files_to_check = [
        'lotto_data.json',
        'lotto_data.json.bak',
        'verification_results_4wins.json',
        'shops_4wins.json'
    ]
    
    for fname in files_to_check:
        try:
            with open(fname, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            total = len(data)
            pov_count = 0
            
            # Data structure might differ
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        if 'pov' in item:
                            pov_count += 1
                        elif 'roadview' in item: # Maybe stored as roadview?
                             pov_count += 1
            
            print(f"File: {fname}")
            print(f"  Total items: {total}")
            print(f"  Items with 'pov': {pov_count}")
            
        except FileNotFoundError:
            print(f"File: {fname} (Not Found)")
        except Exception as e:
            print(f"File: {fname} (Error: {e})")

if __name__ == "__main__":
    inspect_pov_status()
