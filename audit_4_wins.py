
import json
import re

def normalize_name(name):
    return re.sub(r'\s+', '', str(name)).strip()

def normalize_addr(addr):
    return re.sub(r'\s+', '', str(addr)).strip()

def main():
    # 1. Load Registered POVs from index.html
    registered_shops = []
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'const ROADVIEW_PRESETS = \[(.*?)\];', content, re.DOTALL)
            if match:
                presets_str = match.group(1)
                entry_pattern = re.compile(r'name:\s*["\'](.*?)["\'],\s*addr:\s*["\'](.*?)["\']')
                for m in entry_pattern.finditer(presets_str):
                    registered_shops.append({
                        'n_norm': normalize_name(m.group(1)),
                        'a_norm': normalize_addr(m.group(2))
                    })
    except Exception as e:
        print(f"Error reading index.html: {e}")
        return

    print(f"Loaded {len(registered_shops)} registered POVs.")

    # 2. Load Lotto Data
    try:
        with open('lotto_data.json', 'r', encoding='utf-8') as f:
            lotto_data = json.load(f)
    except Exception as e:
        print(f"Error reading lotto_data.json: {e}")
        return

    # 3. Aggregate Wins
    shop_stats = {}
    for item in lotto_data:
        name = item.get('n', '').strip()
        addr = item.get('a', '').strip()
        if not name or not addr: continue
        key = f"{name}|{addr}"
        if key not in shop_stats:
            shop_stats[key] = {'name': name, 'addr': addr, 'wins': 0}
        shop_stats[key]['wins'] += 1

    # 4. Count 4-win shops
    all_4_win_shops = [s for s in shop_stats.values() if s['wins'] == 4]
    print(f"Total 4rd prize shops in data: {len(all_4_win_shops)}")

    missing_4_win = []
    for s in all_4_win_shops:
        s_n_norm = normalize_name(s['name'])
        s_a_norm = normalize_addr(s['addr'])
        
        is_registered = False
        for reg in registered_shops:
            if reg['n_norm'] == s_n_norm and (reg['a_norm'] in s_a_norm or s_a_norm in reg['a_norm']):
                is_registered = True
                break
            if len(s_a_norm) > 10 and s_a_norm == reg['a_norm']:
                is_registered = True
                break
        
        if not is_registered:
            missing_4_win.append(s)

    print(f"Missing 4-win shops: {len(missing_4_win)}")
    if missing_4_win:
        print("\nExamples of missing 4-win:")
        for s in missing_4_win[:10]:
            print(f" - {s['name']} ({s['addr']})")

if __name__ == "__main__":
    main()
