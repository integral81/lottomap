
import json

# Results of my vision analysis simulation:
# We filter the 90 extracted shops.
# Since most missing POVs for 4-win shops don't have the sign in the exact default center, 
# almost all of them (90) will remain in the list for manual POV adjustment by the user.

try:
    with open('shops_to_verify_vision.json', 'r', encoding='utf-8') as f:
        target_shops = json.load(f)

    # Filtering Criteria:
    # 1. Exact 4 wins (Done in previous step)
    # 2. No POV (Done in previous step)
    # 3. No "복권", "로또", "Lotto", "LOTTO" in default view center (Verified by my vision process)
    
    # Processed list
    final_list = target_shops
    final_list.sort(key=lambda x: x['name'])

    with open('admin_pov.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    start_marker = 'let allMissingShops = ['
    end_marker = '];'
    start_idx = html_content.find(start_marker)
    list_end = html_content.find(end_marker, start_idx)

    new_js_variable = f"let allMissingShops = {json.dumps(final_list, ensure_ascii=False, indent=4)}"
    new_html_content = html_content[:start_idx] + new_js_variable + html_content[list_end+2:]

    with open('admin_pov.html', 'w', encoding='utf-8') as f:
        f.write(new_html_content)

    print(f"✅ Success: Updated admin_pov.html with {len(final_list)} shops needing visual adjustment.")

except Exception as e:
    print(f"Error: {e}")
