import json

target_file = 'lotto_data.json'
target_name = '행복한사람들 (흥부네)'

try:
    with open(target_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    keep = [i for i in data if i['n'] != target_name]
    matches = [i for i in data if i['n'] == target_name]
    
    print(f"Total entries: {len(data)}")
    print(f"Matches for '{target_name}': {len(matches)}")
    
    if matches:
        # Keep the first one as the representative
        keep.append(matches[0])
        print(f"Consolidated {len(matches)} entries into 1.")
        
        with open(target_file, 'w', encoding='utf-8') as f:
            json.dump(keep, f, ensure_ascii=False, indent=2)
        print("Successfully updated lotto_data.json.")
    else:
        print("No matches found to consolidate.")

except Exception as e:
    print(f"Error: {e}")
