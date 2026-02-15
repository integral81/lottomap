
import json
import os
import re

LOTTO_DATA_PATH = 'lotto_data.json'
RESULTS_PATH = 'double_check_results.json'

def clean_name(name):
    return re.sub(r'\(.*?\)', '', name).strip()

def get_locality(addr):
    parts = addr.split()
    if len(parts) >= 3:
        return f"{parts[1]} {parts[2]}" # e.g. "장성군 장성읍"
    elif len(parts) >= 2:
        return parts[1]
    return addr

def get_numbers(addr):
    # Extract strings like "1021-3" or "127"
    nums = re.findall(r'\d+-\d+|\d+', addr)
    return [n for n in nums if len(n) >= 2] # Avoid single digits

def main():
    with open(LOTTO_DATA_PATH, 'r', encoding='utf-8') as f:
        lotto_data = json.load(f)
    
    with open(RESULTS_PATH, 'r', encoding='utf-8-sig') as f:
        results = json.load(f)
    
    batch = results[0:50]
    
    stats = {'closed': 0, 'updated': 0, 'matches': 0, 'no_matches': 0}
    
    for item in batch:
        target_name = item['shop_name']
        target_addr = item['target_shop_address']
        status = item['double_check']
        comment = item['comment']
        
        c_target_name = clean_name(target_name)
        target_locality = get_locality(target_addr)
        target_nums = get_numbers(target_addr)
        
        matches = []
        for idx, entry in enumerate(lotto_data):
            e_name = entry.get('n', '')
            e_addr = entry.get('a', '')
            c_e_name = clean_name(e_name)
            
            # Name match (partial or exact)
            if c_target_name in c_e_name or c_e_name in c_target_name:
                # Resolve by address
                # 1. Check numeric parts (strong)
                if any(n in e_addr for n in target_nums):
                    matches.append(idx)
                    continue
                # 2. Check locality (city/district)
                if target_locality in e_addr:
                    matches.append(idx)
                    continue
                # Special case: if name matches exactly and is unique enough, maybe it's a match?
                # But let's stay conservative for accuracy.

        if not matches:
            stats['no_matches'] += 1
            with open('unmatched_batch_01.txt', 'a', encoding='utf-8') as elog:
                elog.write(f"{target_name} | {target_addr}\n")
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
    
    summary = {
        "batch_size": len(batch),
        "shops_closed_identified": stats['closed'],
        "shops_relocated_flagged": stats['updated'],
        "total_data_entries_affected": stats['matches'],
        "unmatched_shops": stats['no_matches']
    }
    print(json.dumps(summary))

if __name__ == "__main__":
    main()
