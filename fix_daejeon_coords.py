
import json

def fix_coords():
    files_to_fix = ['lotto_data.json', 'top_shops_audit.json']
    
    target_lat = 36.3686
    target_lng = 127.3777
    
    for fpath in files_to_fix:
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"Error loading {fpath}: {e}")
            continue

        count = 0
        for entry in data:
            name = entry.get('n', entry.get('name', ''))
            addr = entry.get('a', entry.get('addr', ''))
            
            if '복권명당' in name and '만년동 112' in addr:
                entry['lat'] = target_lat
                entry['lng'] = target_lng
                count += 1
                
        if count > 0:
            with open(fpath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Successfully updated {count} entries in {fpath}.")
        else:
            print(f"No matching entries found in {fpath}.")

if __name__ == "__main__":
    fix_coords()
