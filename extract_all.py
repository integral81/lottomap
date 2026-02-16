
import json
import re

def extract_all():
    files = ['commit_42_povs_utf8.txt', 'commit_golden_pig_utf8.txt']
    all_objects = []
    
    for fname in files:
        try:
            with open(fname, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Regex to find JSON-like objects starting with { and containing "name"
            # We look for { ... } blocks. Simple parser.
            
            lines = content.split('\n')
            buffer = ""
            in_object = False
            
            for line in lines:
                clean_line = line.strip()
                # Remove git diff markers
                if clean_line.startswith('+') or clean_line.startswith('-'):
                    clean_line = clean_line[1:].strip()
                
                if clean_line.startswith('{'):
                    in_object = True
                    buffer = clean_line
                elif in_object:
                    buffer += "\n" + clean_line
                    if clean_line.startswith('}'): # tailored for } or },
                        in_object = False
                        # Try parsing as JSON (remove trailing comma if needed)
                        json_str = buffer.strip().rstrip(',')
                        try:
                            # Fix keys to be quoted if they aren't (usually they are in this project)
                            obj = json.loads(json_str) 
                            all_objects.append(obj)
                        except:
                            # Fallback: manually parse name/address
                            if '"name":' in json_str:
                                all_objects.append({"raw": json_str})
                        
        except Exception as e:
            print(f"Error processing {fname}: {e}")
            
    # Filter for interesting ones
    targets = [
        "황금복권방", "복권명당", "가판점", "GS25", "목화휴게소", 
        "cu", "복권판매점", "뉴빅마트", "대박찬스", "로또휴게실"
    ]
    
    found = []
    for obj in all_objects:
        # Check if object is a dict and has name
        name = ""
        if isinstance(obj, dict):
            name = obj.get('name', '')
            if not name and 'raw' in obj:
                # Extract name from raw string
                m = re.search(r'"name":\s*"([^"]+)"', obj['raw'])
                if m: name = m.group(1)
        
        # Check against targets
        for t in targets:
            if t in name:
                found.append(obj)
                break
                
    with open('recovered_history.json', 'w', encoding='utf-8') as f:
        json.dump(found, f, indent=2, ensure_ascii=False)
        
    print(f"Extracted {len(found)} relevant objects to recovered_history.json")

if __name__ == "__main__":
    extract_all()
