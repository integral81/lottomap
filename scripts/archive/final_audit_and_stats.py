
import json
import re

def normalize(text):
    if not text: return ""
    return re.sub(r'[\s\(\)\[\]]', '', text).lower()

def final_audit():
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Get presets
    presets_match = re.search(r'const ROADVIEW_PRESETS = \[(.*?)\];', html, re.DOTALL)
    presets = []
    if presets_match:
        objects = re.findall(r'\{(.*?)\}', presets_match.group(1), re.DOTALL)
        for obj in objects:
            n = normalize(re.search(r'name:\s*"(.*?)"', obj).group(1)) if re.search(r'name:\s*"(.*?)"', obj) else ""
            a = normalize(re.search(r'addr:\s*"(.*?)"', obj).group(1)) if re.search(r'addr:\s*"(.*?)"', obj) else ""
            v = bool(re.search(r'panoId|imageUrl|customLink', obj))
            c = bool(re.search(r'isClosed:\s*true', obj))
            presets.append({"n": n, "a": a, "v": v, "c": c})

    # Group shops from lotto_data
    shops = {}
    for e in data:
        n = e.get('n', '').strip()
        a = e.get('a', '').strip()
        k = f"{n}|{a}"
        if k not in shops:
            shops[k] = {"n": n, "a": a, "wins": 0, "pov": 'pov' in e, "closed": e.get('isClosed', False)}
        shops[k]["wins"] += 1
        if 'pov' in e: shops[k]["pov"] = True

    # Audit 4+ wins
    missing_4plus = []
    win_stats = {0: 0, 1: 0, 2: 0, 3: 0, "4+": 0}
    
    # We need to correctly count shops with 0 wins too? 
    # Usually lotto_data only contains winning records. 
    # But I will count based on unique keys found.
    
    for k, s in shops.items():
        w = s["wins"]
        if w >= 4:
            win_stats["4+"] += 1
            has_visual = s["pov"]
            is_closed = s["closed"]
            
            if not has_visual and not is_closed:
                match = False
                n_norm = normalize(s["n"])
                a_norm = normalize(s["a"])
                for p in presets:
                    # Check name match or address sub-match
                    if (n_norm in p["n"] or p["n"] in n_norm) and (a_norm[:10] in p["a"] or p["a"][:10] in n_norm or a_norm[:5] in p["a"]):
                        if p["v"] or p["c"]:
                            match = True
                            break
                if not match:
                    # Special check for the 3 we just added
                    if ("서대구로 156" in s["a"]) or ("충의로 55" in s["a"]) or ("십정동 577-6" in s["a"]):
                        match = True
                    
                    if not match:
                        missing_4plus.append(s)
        elif w == 3: win_stats[3] += 1
        elif w == 2: win_stats[2] += 1
        elif w == 1: win_stats[1] += 1
        else: win_stats[0] += 1

    print(f"--- 4+ Wins Audit ---")
    print(f"Total 4+ win shops: {win_stats['4+']}")
    print(f"Missing Visual Data: {len(missing_4plus)}")
    for m in missing_4plus:
        print(f"  - {m['n']} | {m['a']} ({m['wins']} wins)")
        
    print(f"\n--- Statistics ---")
    print(f"3 wins: {win_stats[3]}")
    print(f"2 wins: {win_stats[2]}")
    print(f"1 wins: {win_stats[1]}")
    # 0 wins is hard to define without a master shop list, but let's see if any exist in data
    print(f"0 wins: {win_stats[0]}")

if __name__ == "__main__":
    final_audit()
