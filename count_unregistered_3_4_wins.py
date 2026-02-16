import json
import re
import os

def normalize(text):
    if not text: return ""
    return re.sub(r'\s+', '', str(text)).strip()

def load_index_presets():
    presets = []
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
            # Robust Parsing: Find all { name: "...", addr: "..." } patterns globally
            matches = re.finditer(r'name:\s*"([^"]+)",\s*addr:\s*"([^"]+)"', content)
            for m in matches:
                name = m.group(1).strip()
                addr = m.group(2).strip()
                presets.append({'name': name, 'addr': addr})
    except Exception as e:
        print(f"Error reading index.html: {e}")
    return presets

def main():
    try:
        with open('lotto_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("lotto_data.json not found.")
        return

    # Aggregate Wins
    shop_stats = {}
    for entry in data:
        name = entry.get('n', '').strip()
        addr = entry.get('a', '').strip()
        if not name or not addr: continue
        if "인터넷" in name or "동행복권" in addr: continue
        
        key = normalize(addr)
        if key not in shop_stats:
            shop_stats[key] = {
                'name': name,
                'address': addr,
                'wins': 0
            }
        shop_stats[key]['wins'] += 1

    targets_4 = [s for s in shop_stats.values() if s['wins'] == 4]
    targets_3 = [s for s in shop_stats.values() if s['wins'] == 3]

    print(f"Total shops with 4 wins: {len(targets_4)}")
    print(f"Total shops with 3 wins: {len(targets_3)}")

    # Exclude Registered
    presets = load_index_presets()
    registered_names = [p['name'] for p in presets]
    registered_addrs = [normalize(p['addr']) for p in presets]
    
    unregistered_4 = filter_registered(targets_4, registered_names, registered_addrs)
    unregistered_3 = filter_registered(targets_3, registered_names, registered_addrs)
    
    print(f"Unregistered 4-win shops: {len(unregistered_4)}")
    print(f"Unregistered 3-win shops: {len(unregistered_3)}")

def filter_registered(targets, registered_names, registered_addrs):
    filtered = []
    for t in targets:
        t_name = t['name']
        t_name_norm = normalize(t_name)
        t_addr_norm = normalize(t['address'])
        
        is_name_match = False
        for r_name in registered_names:
            r_name_norm = normalize(r_name)
            if len(t_name_norm) <= 2 or len(r_name_norm) <= 2:
                if t_name_norm == r_name_norm:
                    is_name_match = True
                    break
                continue
            if t_name_norm in r_name_norm or r_name_norm in t_name_norm:
                is_name_match = True
                break
        if is_name_match: continue
            
        is_registered = False
        for r_addr in registered_addrs:
            if len(r_addr) < 5: continue
            if t_addr_norm in r_addr or r_addr in t_addr_norm:
                is_registered = True
                break
        if is_registered: continue
            
        filtered.append(t)
    return filtered

if __name__ == "__main__":
    main()
