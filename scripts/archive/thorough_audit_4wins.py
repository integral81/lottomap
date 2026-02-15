
import json
import re
import os

def audit_shops():
    data_path = 'lotto_data.json'
    html_path = 'index.html'

    if not os.path.exists(data_path) or not os.path.exists(html_path):
        print("Required files (lotto_data.json or index.html) not found.")
        return

    # 1. Load lotto_data.json
    with open(data_path, 'r', encoding='utf-8') as f:
        lotto_data = json.load(f)

    # 2. Extract presets from index.html
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Find ROADVIEW_PRESETS array in JS
    presets_match = re.search(r'const ROADVIEW_PRESETS = \[(.*?)\];', html_content, re.DOTALL)
    presets_list = []
    if presets_match:
        presets_str = presets_match.group(1)
        # Simple extraction using regex for objects
        objects = re.findall(r'\{(.*?)\}', presets_str, re.DOTALL)
        for obj in objects:
            name_match = re.search(r'name:\s*"(.*?)"', obj)
            addr_match = re.search(r'addr:\s*"(.*?)"', obj)
            pano_match = re.search(r'panoId:\s*(\d+)', obj)
            img_match = re.search(r'imageUrl:\s*"(.*?)"', obj)
            closed_match = re.search(r'isClosed:\s*true', obj)
            link_match = re.search(r'customLink:\s*"(.*?)"', obj)
            
            p_name = name_match.group(1) if name_match else ""
            p_addr = addr_match.group(1) if addr_match else ""
            p_has_visual = bool(pano_match or img_match or link_match)
            is_closed = bool(closed_match)
            
            presets_list.append({
                "name": p_name,
                "addr": p_addr,
                "has_visual": p_has_visual,
                "is_closed": is_closed
            })

    # 3. Group wins by Name + Address
    shop_stats = {}
    for entry in lotto_data:
        name = entry.get('n', '').strip()
        addr = entry.get('a', '').strip()
        key = f"{name}|{addr}"
        
        if key not in shop_stats:
            shop_stats[key] = {
                "name": name,
                "addr": addr,
                "wins": 0,
                "has_pov_in_data": False,
                "is_closed_in_data": entry.get('isClosed', False)
            }
        
        shop_stats[key]["wins"] += 1
        if 'pov' in entry and entry['pov']:
            shop_stats[key]["has_pov_in_data"] = True
        if entry.get('isClosed'):
            shop_stats[key]["is_closed_in_data"] = True

    # 4. Perform Audit
    missing_pov_shops = []
    registered_count = 0
    total_4plus = 0

    for key, shop in shop_stats.items():
        if shop["wins"] >= 4:
            total_4plus += 1
            has_visual = shop["has_pov_in_data"]
            is_closed = shop["is_closed_in_data"]

            # If not in data, check presets
            if not has_visual and not is_closed:
                for preset in presets_list:
                    # Match name exactly and address partially
                    if shop["name"] == preset["name"]:
                        # Soft match for address (e.g. "서울" in "서울 강동구...")
                        # We use 5 characters to avoid too broad matches
                        addr_part = shop["addr"][:10]
                        if addr_part in preset["addr"] or preset["addr"] in shop["addr"]:
                            if preset["has_visual"]:
                                has_visual = True
                            if preset["is_closed"]:
                                is_closed = True
                            break

            if has_visual or is_closed:
                registered_count += 1
            else:
                missing_pov_shops.append(shop)

    # 5. Output Report
    print(f"--- 4+ Wins POV Audit Report ---")
    print(f"Total shops with 4+ wins: {total_4plus}")
    print(f"Successfully registered (POV/Image/Closed): {registered_count}")
    print(f"Missing Visual Data: {len(missing_pov_shops)}")
    print("-" * 40)

    if missing_pov_shops:
        missing_pov_shops.sort(key=lambda x: x['wins'], reverse=True)
        for i, shop in enumerate(missing_pov_shops[:50], 1):
            print(f"{i}. [{shop['wins']} wins] {shop['name']} - {shop['addr']}")
        if len(missing_pov_shops) > 50:
            print(f"... and {len(missing_pov_shops) - 50} more.")
    else:
        print("All 4+ win shops have POVs or are accounted for!")

if __name__ == "__main__":
    audit_shops()
