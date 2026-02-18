
import json
import subprocess
import sys
import os

# Ensure UTF-8
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

def search_history(query):
    # Search in double_check_results.json
    results = []
    try:
        with open('double_check_results.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                if query in item.get('shop_name', '') or query in item.get('target_shop_address', ''):
                    results.append(f"[DoubleCheck] {item.get('shop_name')}: {item.get('double_check')} ({item.get('comment')})")
    except: pass
    
    # Search in verification_results_all.json
    try:
        with open('verification_results_all.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            # This file is large, might need a more efficient way if it fails
            for item in data:
                if query in str(item):
                    results.append(f"[Verification] Found mention: {item.get('shop_name', 'Unknown')}")
    except: pass
    
    return results

def deep_research_candidates():
    with open('merge_candidates.json', 'r', encoding='utf-8') as f:
        candidates = json.load(f)
    
    final_report = []
    
    for c in candidates[10:20]: # Process batch 2 (11-20)
        name = c['name']
        addrs = c['addrs']
        
        history_findings = []
        for addr in addrs:
            # Search part of the address (e.g., the specific numbers)
            addr_query = addr.split(' ')[-2:] # Usually the dong/number part
            addr_query = ' '.join(addr_query)
            history_findings.extend(search_history(addr_query))
        
        if name != "-":
            history_findings.extend(search_history(name))
            
        history_findings = list(set(history_findings))
        
        c['history'] = history_findings
        final_report.append(c)
        
    return final_report

results = deep_research_candidates()

for i, r in enumerate(results, 1):
    print(f"[{i}] 매장명: {r['name']}")
    print(f"    - 주소들: {r['addrs']}")
    print(f"    - 당첨회차: {r['rounds']}")
    if r['history']:
        print(f"    - [LOCAL HISTORY]:")
        for h in r['history']:
            print(f"      * {h}")
    else:
        print(f"    - [LOCAL HISTORY]: No direct match found. Needs Deep Search.")
    print("-" * 50)
