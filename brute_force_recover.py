
import re
import json

def brute_force_extract():
    print("--- BRUTE FORCE EXTRACTION ---")
    files = ['lotto_data_old.json', 'lotto_data_older.json', 'lotto_data_clean.json']
    
    found_targets = []
    
    for fname in files:
        print(f"Scanning {fname}...")
        try:
            with open(fname, 'rb') as f:
                content = f.read().decode('utf-8', errors='ignore')
                
            # Naive regex to find JSON objects containing "로또휴게실"
            # Looking for { ... "n": "로또휴게실" ... }
            # We'll use a wide capture and try to parse
            
            # Pattern: find generic object start/end surrounding the name
            # This is tricky with nested structures, but we know the structure is flat list of objects
            # So looking for { [^}]+ "n":\s*"로또휴게실" [^}]+ }
            
            pattern = r'\{[^{}]*"n":\s*"로또휴게실"[^{}]*\}'
            matches = re.findall(pattern, content)
            
            for m in matches:
                try:
                    # Clean up any potential bad chars
                    clean_m = re.sub(r'[\x00-\x1f]', '', m)
                    obj = json.loads(clean_m)
                    if obj.get('pov'):
                        print(f"!!! FOUND POV IN {fname} !!!")
                        print(json.dumps(obj, indent=2, ensure_ascii=False))
                        found_targets.append(obj)
                except:
                    pass
                    
        except Exception as e:
            print(f"Error scanning {fname}: {e}")
            
    if found_targets:
        print(f"\nTotal Confirmed POV Records Found: {len(found_targets)}")
        with open('salvaged_data.json', 'w', encoding='utf-8') as f:
            json.dump(found_targets, f, indent=2, ensure_ascii=False)
    else:
        print("\nNo valid POV records found using brute force.")

if __name__ == "__main__":
    brute_force_extract()
