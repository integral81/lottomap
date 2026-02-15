import json
import re

def audit_pov():
    # 1. Load lotto_data.json
    try:
        with open('lotto_data.json', 'r', encoding='utf-8') as f:
            lotto_data = json.load(f)
    except FileNotFoundError:
        print("Error: lotto_data.json not found.")
        return

    # 2. Identify shops with 5+ wins
    shop_wins = {}
    shop_coords = {}
    for entry in lotto_data:
        name = entry.get('n', '').strip()
        addr = entry.get('a', '').strip()
        if not name or not addr:
            continue
        key = f"{name}|{addr}"
        shop_wins[key] = shop_wins.get(key, 0) + 1
        
        # Store coordinates if available
        if 'lat' in entry and 'lng' in entry:
            shop_coords[key] = {'lat': entry['lat'], 'lng': entry['lng']}

    high_win_shops = {k: v for k, v in shop_wins.items() if v >= 5}
    print(f"Total shops with 5+ wins: {len(high_win_shops)}")

    # 3. Extract ROADVIEW_PRESETS from index.html
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print("Error: index.html not found.")
        return

    # Using regex to find the ROADVIEW_PRESETS array block
    presets_match = re.search(r'const ROADVIEW_PRESETS = \[(.*?)\];', html_content, re.DOTALL)
    if not presets_match:
        print("Error: Could not find ROADVIEW_PRESETS in index.html")
        return

    presets_text = presets_match.group(1)
    # Extract name and addr using regex from the presets text
    # Pattern: { name: "...", addr: "...", ... }
    registered_shops = []
    preset_items = re.findall(r'\{\s*name:\s*"([^"]+)",\s*addr:\s*"([^"]+)"', presets_text)
    for name, addr in preset_items:
        registered_shops.append(f"{name.strip()}|{addr.strip()}")

    print(f"Total POV registered shops in index.html: {len(registered_shops)}")

    # 4. Cross-reference
    missing_pov = []
    for key, wins in high_win_shops.items():
        # Check if Name|Addr is in registered_shops
        # Since addresses might vary slightly (e.g. road name vs old addr), 
        # let's check for partial matches or normalized matches if needed.
        # For now, let's start with exact match.
        
        found = False
        name_lotto, addr_lotto = key.split('|')
        
        for reg in registered_shops:
            name_reg, addr_reg = reg.split('|')
            # Check if Name matches AND (Address matches exactly OR Address is contained)
            if name_lotto == name_reg:
                if addr_lotto == addr_reg or addr_lotto in addr_reg or addr_reg in addr_lotto:
                    found = True
                    break
        
        if not found:
            coords = shop_coords.get(key, {})
            missing_pov.append({
                "name": name_lotto,
                "address": addr_lotto,
                "wins": wins,
                "lat": coords.get('lat'),
                "lng": coords.get('lng'),
                "has_coords": "lat" in coords
            })

    # Sort by wins descending
    missing_pov.sort(key=lambda x: x['wins'], reverse=True)

    # 5. Save Summary Report
    summary = {
        "total_high_win_shops": len(high_win_shops),
        "total_registered_pov": len(registered_shops),
        "missing_pov_count": len(missing_pov),
        "missing_list": missing_pov
    }

    with open('audit_5wins_summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"Audit complete. Found {len(missing_pov)} shops missing POV data.")
    print("Report saved to audit_5wins_summary.json")

if __name__ == "__main__":
    audit_pov()
