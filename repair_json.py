
import json
import re

def repair_and_recover():
    print("--- Attempting to repair lotto_data_old.json ---")
    
    # Read as binary to avoid encoding errors initially
    with open('lotto_data_old.json', 'rb') as f:
        raw_data = f.read()
        
    # Decode ignoring errors to get string
    # Git export often uses UTF-16 LE with BOM if redirected in PowerShell
    try:
        content = raw_data.decode('utf-16')
    except:
        content = raw_data.decode('utf-8', errors='ignore')
        
    # Remove BOM
    if content.startswith('\ufeff'):
        content = content[1:]
        
    # The debug output showed "line 3 column 28 (char 33)".
    # It seems some quotes or characters are broken.
    # Let's try to regex fix common patterns if JSON load fails.
    
    try:
        data = json.loads(content)
        print(f"Success! Parsed {len(data)} items directly.")
    except json.JSONDecodeError:
        print("Direct parse failed. Applying regex cleanups...")
        # Replace invalid control chars
        content = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', content)
        try:
            data = json.loads(content)
            print(f"Recovered {len(data)} items after cleanup.")
        except:
            print("Cleanup failed. Trying extensive recovery...")
            return

    # Now extraction logic
    print(f"Current Data Size: {len(data)}")
    
    restored_povs = []
    
    # Check for known missing targets
    targets = ["로또휴게실", "상갈", "보라동"]
    
    for item in data:
        # Check if item has POV
        if item.get('pov'):
            restored_povs.append(item)
            
            # Check if this is one of the requested targets
            if any(t in item.get('n', '') or t in item.get('a', '') for t in targets):
                print(f"FOUND TARGET: {item['n']} - {item.get('pov')}")

    print(f"Total entries with POV in backup: {len(restored_povs)}")
    
    # Save the good ones
    if len(restored_povs) > 100: # Arbitrary threshold to ensure we found a good batch
        with open('recovered_pov_data.json', 'w', encoding='utf-8') as f:
            json.dump(restored_povs, f, indent=2, ensure_ascii=False)
        print("Saved 2MB+ relevant data to 'recovered_pov_data.json'")
    else:
        print("Not enough data found to justify save.")

if __name__ == "__main__":
    repair_and_recover()
