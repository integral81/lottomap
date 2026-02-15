
import os

filepath = 'index.html'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
found_first = False
in_presets = False

# We know presets list starts around line 2500 and ends around 2620
for i, line in enumerate(lines):
    # Check if we are in the presets list
    if 'const ROADVIEW_PRESETS = [' in line:
        in_presets = True
    
    if 'panoId: 1197759123' in line:
        if in_presets and not found_first:
            # This is the correct one, keep it
            new_lines.append(line)
            found_first = True
            print(f"Keeping correct entry at line {i+1}")
        else:
            # This is a duplicate or misplaced entry, skip it
            print(f"Removing corrupted entry at line {i+1}")
            continue
    else:
        new_lines.append(line)
        
    if '];' in line and in_presets:
        in_presets = False

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print("Cleanup complete.")
