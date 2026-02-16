
import json
import os

def check_file(filename):
    print(f"--- Checking {filename} ---")
    if not os.path.exists(filename):
        print("File not found.")
        return

    content = None
    encodings = ['utf-8', 'utf-16', 'utf-16-le', 'cp949', 'latin1']
    
    for enc in encodings:
        try:
            with open(filename, 'r', encoding=enc) as f:
                content = f.read()
            print(f"Successfully read with {enc}")
            break
        except Exception as e:
            print(f"Failed with {enc}: {e}")
            
    if content:
        try:
            # Handle potential BOM or git diff artifacts if any
            if content.startswith('\ufeff'):
                content = content[1:]
                
            data = json.loads(content)
            print(f"JSON Parsed Successfully. Total items: {len(data)}")
            
            pov_count = len([x for x in data if x.get('pov')])
            print(f"Entries with POV: {pov_count}")
            
            target = [x for x in data if '로또휴게실' in x['n']]
            if target:
                print(f"Found '로또휴게실': {target[0]}")
            else:
                print("'로또휴게실' not found.")
                
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            print(f"First 100 chars: {content[:100]}")

if __name__ == "__main__":
    check_file('lotto_data.json')
    check_file('lotto_data_old.json') 
    check_file('lotto_data_older.json')
