
import json
import re

def find_missing_5wins():
    # 1. Load Presets from index.html
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            html = f.read()
    except:
        print("index.html not found")
        return

    match = re.search(r'const ROADVIEW_PRESETS = \[(.*?)\];', html, re.DOTALL)
    existing_presets = set()
    if match:
        presets_raw = match.group(1)
        # Match only the names to avoid complex object parsing
        names = re.findall(r'name:\s*"(.*?)"', presets_raw)
        existing_presets = set(names)

    # 2. Load current 5+ win shops from lotto_data.json
    try:
        with open('lotto_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        print("lotto_data.json not found")
        return

    counts = {}
    for d in data:
        # Key: (Name, Address, Lat, Lng)
        k = (d['n'], d['a'], d.get('lat'), d.get('lng'))
        counts[k] = counts.get(k, 0) + 1

    five_plus = []
    for k, v in counts.items():
        if v >= 5:
            five_plus.append({
                'n': k[0],
                'a': k[1],
                'lat': k[2],
                'lng': k[3],
                'w': v
            })

    # 3. Identify missing shops
    missing = [s for s in five_plus if s['n'] not in existing_presets]
    
    # Sort by win count descending
    missing.sort(key=lambda x: x['w'], reverse=True)

    print(f"Total 5+ win shops: {len(five_plus)}")
    print(f"Shops already in Presets: {len(existing_presets)}")
    print(f"New 5+ win shops missing from Presets: {len(missing)}")
    
    if missing:
        with open('top_shops_missing_5wins.json', 'w', encoding='utf-8') as f:
            json.dump(missing, f, indent=2, ensure_ascii=False)
        print("Saved missing shops to 'top_shops_missing_5wins.json'")

if __name__ == "__main__":
    find_missing_5wins()
