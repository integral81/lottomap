
import json
import os
import re

LOTTO_DATA_PATH = 'lotto_data.json'
RESULTS_PATH = 'double_check_results.json'

def clean_name(name):
    if not name: return ""
    name = name.upper().replace('씨유', 'CU').replace('지에스', 'GS')
    return re.sub(r'[\s\(\)\&\-\_\.\,]', '', name)

def get_numbers(addr):
    if not addr: return set()
    return set(re.findall(r'\d+-\d+|\d+', addr))

def get_locality(addr):
    if not addr: return set()
    # Focus on Town/Village/City/District
    return set(re.findall(r'[가-힣]+(?:동|리|읍|면|구|시|군)', addr))

def main():
    with open(LOTTO_DATA_PATH, 'r', encoding='utf-8') as f:
        lotto_data = json.load(f)
    
    with open(RESULTS_PATH, 'r', encoding='utf-8-sig') as f:
        results = json.load(f)
    
    # Process from index 411 to end
    batch = results[411:]
    
    ambiguous = []
    auto_stats = {'closed': 0, 'relocated': 0, 'open_verified': 0}
    
    # Track updated indices to avoid redundant work
    updated_count = 0

    for idx_in_results, item in enumerate(batch):
        real_idx = idx_in_results + 411
        name = item['shop_name']
        addr = item['target_shop_address']
        status = item['double_check']
        comment = item.get('comment', '')
        
        # We only care about shops that need status changes
        is_closing = (status == 'CLOSED')
        is_moving = (status == 'RELOCATED' or ('이전' in comment and '확인' in comment))
        
        if not is_closing and not is_moving:
            auto_stats['open_verified'] += 1
            continue

        c_name = clean_name(name)
        nums = get_numbers(addr)
        locals = get_locality(addr)
        
        matches = []
        for d_idx, entry in enumerate(lotto_data):
            e_name = clean_name(entry.get('n', ''))
            e_addr = entry.get('a', '')
            
            # 1. Name must be very similar
            if c_name not in e_name and e_name not in c_name:
                continue
            
            # 2. Strong match: Address numbers (e.g. 127-11) match
            e_nums = get_numbers(e_addr)
            if nums and (nums & e_nums):
                matches.append(d_idx)
                continue
            
            # 3. Alternative match: Town level match
            e_locals = get_locality(e_addr)
            if locals and e_locals:
                # Match town level keywords (동, 리, 읍, 면)
                target_towns = {l for l in locals if l.endswith(('동', '리', '읍', '면'))}
                entry_towns = {l for l in e_locals if l.endswith(('동', '리', '읍', '면'))}
                if target_towns & entry_towns:
                    # If town matches and name matches, it's highly likely
                    matches.append(d_idx)

        # Remove duplicate matches
        matches = list(set(matches))

        # Check Ambiguity
        if not matches:
            ambiguous.append({"idx": real_idx, "reason": "No data match found", "item": item})
            continue
            
        # If matches exist across multiple DIFFERENT address clusters, it might be ambiguous
        unique_addresses = {lotto_data[m]['a'] for m in matches}
        if len(unique_addresses) > 1:
            # Check if they are just minor formatting differences
            if len({clean_string(a) for a in unique_addresses}) > 1:
                 ambiguous.append({"idx": real_idx, "reason": "Multiple data clusters matched", "item": item, "matches": [lotto_data[m] for m in matches]})
                 continue

        # Auto Tag
        if is_closing:
            for m in matches:
                lotto_data[m]['closed'] = True
            auto_stats['closed'] += 1
            updated_count += len(matches)
        elif is_moving:
            for m in matches:
                lotto_data[m]['pending_relocation'] = comment
            auto_stats['relocated'] += 1
            updated_count += len(matches)

    # Save
    with open(LOTTO_DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(lotto_data, f, indent=2, ensure_ascii=False)
    
    print(f"--- AUTO TAGGING COMPLETE (411-END) ---")
    print(f"Successfully CLOSED: {auto_stats['closed']} shops")
    print(f"Successfully RELOCATED tagged: {auto_stats['relocated']} shops")
    print(f"OPEN (No change needed): {auto_stats['open_verified']} shops")
    print(f"Total entries affected: {updated_count}")
    print(f"Ambiguous cases requiring manual check: {len(ambiguous)}")
    
    if ambiguous:
        with open('ambiguous_shops.json', 'w', encoding='utf-8') as f:
            json.dump(ambiguous, f, indent=2, ensure_ascii=False)
        print("Ambiguous list saved to ambiguous_shops.json")

def clean_string(s):
    return re.sub(r'[\s\(\)\&\-\_\.\,]', '', s)

if __name__ == "__main__":
    main()
