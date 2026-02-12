
import json
import os
import re

LOTTO_DATA_PATH = 'lotto_data.json'
RESULTS_PATH = 'double_check_results.json'

def clean_string(s):
    if not s: return ""
    s = s.upper() # Standardize to upper
    # Replace common variations
    s = s.replace('씨유', 'CU').replace('지에스', 'GS')
    # Remove whitespace and special chars
    s = re.sub(r'[\s\(\)\&\-\_\.\,]', '', s)
    return s

def get_addr_numbers(addr):
    # Extract numbers like 1021-3 or 127
    return set(re.findall(r'\d+-\d+|\d+', addr))

def get_locality(addr):
    # Get province/city/district keywords
    parts = re.findall(r'[가-힣]+', addr)
    # Filter for common locality ends
    return {p for p in parts if p.endswith(('동', '리', '읍', '면', '구', '시', '군'))}

def tag_shops(start_idx, end_idx):
    with open(LOTTO_DATA_PATH, 'r', encoding='utf-8') as f:
        lotto_data = json.load(f)
    
    with open(RESULTS_PATH, 'r', encoding='utf-8-sig') as f:
        results = json.load(f)
    
    batch = results[start_idx:end_idx]
    
    stats = {'closed': 0, 'updated': 0, 'matches': 0, 'no_matches': 0}
    failed_items = []

    for item in batch:
        target_name = item['shop_name']
        target_addr = item['target_shop_address']
        status = item['double_check']
        comment = item.get('comment', '')
        
        c_target_name = clean_string(target_name)
        target_nums = get_addr_numbers(target_addr)
        target_localities = get_locality(target_addr)
        
        matches = []
        for idx, entry in enumerate(lotto_data):
            e_name = entry.get('n', '')
            e_addr = entry.get('a', '')
            c_e_name = clean_string(e_name)
            
            # Check for name similarity
            name_match = (c_target_name in c_e_name or c_e_name in c_target_name)
            
            if name_match:
                e_nums = get_addr_numbers(e_addr)
                # Strong check: numeric overlap
                if target_nums & e_nums:
                    matches.append(idx)
                    continue
                # Weak check: Locality overlap
                e_localities = get_locality(e_addr)
                if (target_localities & e_localities):
                    # If we have at least town level match
                    town_match = any(l.endswith(('읍', '면', '동', '리')) for l in (target_localities & e_localities))
                    if town_match:
                        matches.append(idx)

        if not matches:
            stats['no_matches'] += 1
            failed_items.append(f"{target_name} | {target_addr}")
            continue
            
        stats['matches'] += len(matches)
        
        if status == 'CLOSED':
            for idx in matches:
                lotto_data[idx]['closed'] = True
            stats['closed'] += 1
        elif status == 'RELOCATED' or ('이전' in comment and '확인' in comment):
            for idx in matches:
                lotto_data[idx]['pending_relocation'] = comment
            stats['updated'] += 1

    with open(LOTTO_DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(lotto_data, f, indent=2, ensure_ascii=False)
    
    return {
        "processed": len(batch),
        "closed_tags": stats['closed'],
        "relocation_tags": stats['updated'],
        "entriesAffected": stats['matches'],
        "unmatched": stats['no_matches'],
        "failed_list": failed_items
    }

if __name__ == "__main__":
    # To be called with range
    import sys
    if len(sys.argv) == 3:
        start = int(sys.argv[1])
        end = int(sys.argv[2])
        res = tag_shops(start, end)
        print(json.dumps(res, ensure_ascii=False))
