import re
import json

# Read registered shops from index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract ROADVIEW_PRESETS variables
# Assuming format: { name: "Name", ... }
presets = []
matches = re.findall(r'\{ name: "([^"]+)", addr: "([^"]+)"', content)
registered_names = {m[0] for m in matches}

# Read admin targets
with open('admin_targets.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Extract object list from JS
# This is a simple regex extraction, might need adjustment if JS is complex
# adminTargets = [ ... ]
json_str = js_content.split('const adminTargets = ')[1].split(';')[0]
# The JS object keys might not be quoted, which is invalid JSON. 
# We'll use a regex to find names in the JS file directly for simplicity/robustness against bad JSON
target_matches = re.findall(r'"name": "([^"]+)"', js_content)
target_names = set(target_matches)

# Find overlaps
overlaps = registered_names.intersection(target_names)

print(f"Registered count: {len(registered_names)}")
print(f"Target count: {len(target_names)}")
print(f"Overlaps found: {len(overlaps)}")

if overlaps:
    print("Duplicates detected (Registered but still in Admin List):")
    for name in overlaps:
        print(f"- {name}")
else:
    print("No duplicates found.")
