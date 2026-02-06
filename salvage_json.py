import json
import re

def salvage_json(filepath):
    print(f"Attempting to salvage {filepath}...")
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"Failed to read file: {e}")
        return

    # Try to find valid top-level objects in the broken JSON array
    # The format is [{"r":...}, {"r":...}]
    # We can use regex to find all objects
    pattern = r'\{"r":\s*\d+,\s*"n":\s*".*?",\s*"a":\s*".*?",\s*"m":\s*".*?",\s*"lat":\s*[\d\.]+,\s*"lng":\s*[\d\.]+\}'
    matches = re.finditer(pattern, content)
    
    salvaged_data = []
    for match in matches:
        try:
            obj = json.loads(match.group())
            salvaged_data.append(obj)
        except:
            continue
            
    print(f"Salvaged {len(salvaged_data)} records.")
    
    if salvaged_data:
        output_path = "lotto_data_salvaged.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(salvaged_data, f, ensure_ascii=False, indent=2)
        print(f"Saved salvaged data to {output_path}")
        return salvaged_data
    else:
        print("No valid records found for salvage.")
        return None

if __name__ == "__main__":
    salvage_json("lotto_data.json")
