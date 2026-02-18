
import json
import re

def normalize_name(name):
    # Remove all spaces for loose matching
    return re.sub(r'\s+', '', str(name)).strip()

def normalize_addr(addr):
    # Remove all spaces for loose matching
    return re.sub(r'\s+', '', str(addr)).strip()

def main():
    # 1. Load Registered POVs from index.html (ROADVIEW_PRESETS)
    registered_shops = []
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
            # Extract ROADVIEW_PRESETS array
            # Assuming format: const ROADVIEW_PRESETS = [ ... ];
            match = re.search(r'const ROADVIEW_PRESETS = \[(.*?)\];', content, re.DOTALL)
            if match:
                presets_str = match.group(1)
                # Parse each object roughly using regex to find name and addr
                # This handles single quotes, double quotes, and simple escapes
                entry_pattern = re.compile(r'name:\s*["\'](.*?)["\'],\s*addr:\s*["\'](.*?)["\']')
                for m in entry_pattern.finditer(presets_str):
                    registered_shops.append({
                        'n_norm': normalize_name(m.group(1)),
                        'a_norm': normalize_addr(m.group(2)),
                        'raw_name': m.group(1),
                        'raw_addr': m.group(2)
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

    # 3. Aggregate Wins Grouped by Normalized Address (and Name fallback)
    shop_stats = {}
    
    for item in lotto_data:
        name = item.get('n', '').strip()
        addr = item.get('a', '').strip()
        if not name or not addr: continue
        
        # Key by Normalized Address mainly, normalize name secondary
        # If address is very short (e.g. just Dong), maybe use name?
        # Let's stick to Name|Address key for strict grouping first
        key = f"{name}|{addr}"
        
        if key not in shop_stats:
            shop_stats[key] = {
                'name': name,
                'addr': addr,
                'wins': 0
            }
        shop_stats[key]['wins'] += 1

    # 4. Check Registration Status & Count Missing
    missing_counts = {
        3: 0,
        2: 0,
        1: 0,
        0: 0 
    }
    
    # Store some examples for verification
    examples = {3:[], 2:[], 1:[]}

    print(f"Scanning {len(shop_stats)} unique shops vs {len(registered_shops)} presets...")

    for key, shop in shop_stats.items():
        wins = shop['wins']
        if wins > 3: continue # 4+ wins are handled by other scripts, we focus on 3, 2, 1
        
        s_n_norm = normalize_name(shop['name'])
        s_a_norm = normalize_addr(shop['addr'])
        
        is_registered = False
        
        for reg in registered_shops:
            # 1. Exact Name match AND Address overlap
            if reg['n_norm'] == s_n_norm:
                # Check address overlap (one contains the other)
                 if reg['a_norm'] in s_a_norm or s_a_norm in reg['a_norm']:
                     is_registered = True
                     break
            
            # 2. Address Match (Startswith/Endswith/Contains significant part)
            # If address matches exactly (normalized), we assume same shop even if name changed
            if len(s_a_norm) > 5 and s_a_norm == reg['a_norm']:
                 is_registered = True
                 break
                 
            # 3. Handle 'CU', 'GS25' generic names with specific address
            if ('CU' in s_n_norm or 'GS25' in s_n_norm) and '점' in s_n_norm:
                # If chain store name matches exactly
                if reg['n_norm'] == s_n_norm:
                     is_registered = True
                     break

        if not is_registered:
            if wins == 3:
                missing_counts[3] += 1
                examples[3].append(f"{shop['name']} ({shop['addr']})")
            elif wins == 2:
                missing_counts[2] += 1
            elif wins == 1:
                missing_counts[1] += 1
            else:
                 missing_counts[0] += 1

    # Results Output
    print("-" * 40)
    print("      POV 미등록 매장 건수 리포트      ")
    print("-" * 40)
    print(f" [3회 당첨] : {missing_counts[3]} 건")
    print(f" [2회 당첨] : {missing_counts[2]} 건")
    print(f" [1회 당첨] : {missing_counts[1]} 건")
    print("-" * 40)
    
    if missing_counts[3] > 0:
        print("\n[3회 당첨 미등록 예시 (Top 5)]")
        for ex in examples[3][:5]:
            print(f" - {ex}")

if __name__ == "__main__":
    main()
