
import json
import os
import re

def load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def load_text(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return ""

def audit_and_consolidate():
    # 1. Load context
    candidates = load_json('merge_candidates.json')
    data = load_json('lotto_data.json')
    history_dc = load_json('double_check_results.json')
    history_ver = load_json('verification_results_all.json')
    closed_report = load_text('closed_shops_report.md')
    presets = load_text('current_presets.txt')
    
    # Pre-map history for speed
    history_map = {}
    for item in history_dc:
        name = item.get('shop_name', '')
        addr = item.get('target_shop_address', '')
        status = item.get('double_check', '')
        history_map[name] = status
        history_map[addr] = status

    final_merges = []
    closed_detected = []
    
    for c in candidates:
        name = c['name']
        addrs = c['addrs']
        
        # Determine status from history
        is_closed = False
        reason = ""
        
        # Check by name/addr in history strings
        search_terms = [name] + addrs
        for term in search_terms:
            if not term or term == "-": continue
            if f"{term} (폐점)" in presets or f"{term} (폐점)" in closed_report:
                is_closed = True
                reason = "Presets/Report"
                break
            if history_map.get(term) == "CLOSED":
                is_closed = True
                reason = "DoubleCheck"
                break
        
        if is_closed:
            closed_detected.append({"name": name, "addrs": addrs, "reason": reason})
            # Apply closure to data
            for d in data:
                if d.get('n') == name or any(a in d.get('a', '') for a in addrs):
                    d['closed'] = True
                    d['hidden'] = True
            continue

        # If not closed, calculate total unique wins
        # We need to find all raw records in data that match this candidate
        matching_records = []
        for d in data:
            if d.get('n') == name or any(a in d.get('a', '') for a in addrs):
                # Ensure it's not a different shop with same name but far away (safety check)
                matching_records.append(d)
        
        # Collect all unique rounds
        all_rounds = set()
        for r in matching_records:
            if r.get('r'): all_rounds.add(r['r'])
            if r.get('r_list'): all_rounds.update(r['r_list'])
        
        total_wins = len(all_rounds)
        
        if total_wins >= 3:
            final_merges.append({
                "name": name,
                "addrs": addrs,
                "wins": total_wins,
                "rounds": sorted(list(all_rounds))
            })

    # 2. Perform Merges in lotto_data.json
    merged_names = []
    for m in final_merges:
        # Find the best record to keep as primary
        matches = [d for d in data if (d.get('n') == m['name'] or any(a in d.get('a', '') for a in m['addrs'])) and not d.get('closed')]
        if not matches: continue
        
        # Pick one with POV if exists
        primary = next((d for d in matches if d.get('pov')), matches[0])
        
        new_record = primary.copy()
        new_record['r_list'] = m['rounds']
        new_record['count'] = m['wins']
        
        # Remove old ones
        data = [d for d in data if d not in matches]
        data.append(new_record)
        merged_names.append(m['name'])

    # 3. Save results
    with open('lotto_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
    
    # Sync to JS
    js_content = 'const lottoData = ' + json.dumps(data, ensure_ascii=False) + ';';
    with open('lotto_data.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
        
    return final_merges, closed_detected

merges, closed = audit_and_consolidate()
print(f"REPORT: Found {len(closed)} closed shops from history.")
print(f"REPORT: Consolidated {len(merges)} shops with 3+ wins.")
for m in sorted(merges, key=lambda x: x['wins'], reverse=True)[:20]:
    print(f"- {m['name']} ({m['wins']}회): {m['addrs']}")
