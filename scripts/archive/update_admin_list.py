
import json

# Load the new list of 4-win shops
try:
    with open('shops_4wins_missing_pov.json', 'r', encoding='utf-8') as f:
        new_shops = json.load(f)
except Exception as e:
    print(f"Error loading JSON: {e}")
    exit(1)

# Read the HTML file
html_path = 'admin_pov.html'
try:
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
except Exception as e:
    print(f"Error reading HTML: {e}")
    exit(1)

# Prepare the formatted JSON string for the JavaScript variable
# We want it to be nicely indented within the script tag
new_shops_js = json.dumps(new_shops, ensure_ascii=False, indent=16) 
# The indent=16 is a rough guess to match the existing indentation level, 
# but simply replacing the variable assignment is safer.

# Find the start and end of the allMissingShops variable assignment
start_marker = "let allMissingShops = ["
end_marker = "];" # Assuming the list ends with ];

start_idx = html_content.find(start_marker)
if start_idx == -1:
    print("Could not find 'let allMissingShops = [' in HTML")
    exit(1)

# Find the end of the array. searching from start_idx
end_idx = html_content.find(end_marker, start_idx)
if end_idx == -1:
    print("Could not find '];' after start marker")
    exit(1)

# Construct the new content
# We will use a placeholder for the JSON data to avoid indentation issues in python string formatting
new_js_variable = f"let allMissingShops = {json.dumps(new_shops, ensure_ascii=False, indent=4)}"

# Replace the old variable assignment
new_html_content = html_content[:start_idx] + new_js_variable + html_content[end_idx+1:]

# Add the 'Copy Address' button logic to the renderShopList or similar function if it's not already there.
# Looking at the provided admin_pov.html, I need to see where renderShopList is defined.
# It seems I need to read more of the file to do the JS updates properly.
# But I can just rewrite the variable part first.

# Let's perform the safe replacement of the variable first.
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(new_html_content)

print(f"Updated {html_path} with {len(new_shops)} shops.")
