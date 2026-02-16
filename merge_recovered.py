
import json

def merge_recovered_data():
    # 1. Load Recovered
    try:
        with open('recovered_list_mapped.json', 'r', encoding='utf-8') as f:
            recovered = json.load(f)
    except:
        print("No recovered data found.")
        return

    # 2. Load Main Data
    json_path = 'lotto_data.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    print(f"Loaded {len(data)} main records, {len(recovered)} recovered candidates.")
    
    restored_count = 0
    restored_names = []
    
    # Create lookup map for recovered data (by name? risky. by panoId? useless if missing)
    # We need to match recovered items to existing items in data
    # recovering means adding 'pov' to items that lack it.
    
    for rec in recovered:
        # We have 'name', 'addr', 'panoId' in rec
        # Find matching item in data
        
        target_name = rec['name']
        target_id = str(rec['panoId'])
        
        for item in data:
            # Skip if already has POV
            if item.get('pov'): continue
            
            # Name match (fuzzy)
            # rec['name'] often from commit diff which might be partial
            # let's require name to be in item['n']
            
            if target_name in item['n'] or item['n'] in target_name:
                # Region check for safety
                # e.g. check if addr province matches
                # rec['addr'] might be "경남 사천시..."
                # item['a'] might be "경남 사천시..."
                
                # Check region prefix (first 2 chars)
                rec_p = rec.get('addr', '')[:2]
                item_p = item.get('a', '')[:2]
                
                if rec_p and item_p and rec_p == item_p:
                     # Match!
                     item['pov'] = {
                         "id": target_id,
                         "pan": 0, "tilt": 0, "zoom": 0 # Default, better than nothing
                     }
                     # If we had PAN/TILT in the regex search, we should use it.
                     # But current map_recovered_ids.py didn't extract pan/tilt.
                     # The user accepts "exact POV" from history.
                     # I'll check if I can extract pan/tilt later, but for now ID is key.
                     
                     restored_count += 1
                     restored_names.append(item['n'])
                     break
                     
    # Save
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully restored {restored_count} shops.")
    print(f"Sample: {restored_names[:10]}")
    
    # Identify leftovers from the top 10
    top10 = [
        "황금복권방", "복권명당", "가판점", "GS25", "목화휴게소", 
        "cu", "복권판매점", "뉴빅마트", "대박찬스", "로또휴게실"
    ]
    
    print("\n[Top 10 Status]")
    merged_names = " ".join(restored_names)
    for t in top10:
        found_in_merge = any(t in n for n in restored_names)
        # Check if it already had POV
        already_has = False
        for i in data:
            if t in i['n'] and i.get('pov'): already_has = True
            
        status = "MERGED" if found_in_merge else ("EXISTS" if already_has else "MISSING")
        print(f"  {t}: {status}")

if __name__ == "__main__":
    merge_recovered_data()
