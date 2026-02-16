
import json
import re

def update_html():
    # Load candidates
    with open('auto_pilot_candidates.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    # Filter valid
    valid_targets = [d for d in data if d.get('lat')]
    print(f"Found {len(valid_targets)} valid targets.")
    
    # Read HTML
    with open('auto_pov_pilot.html', 'r', encoding='utf-8') as f:
        html = f.read()
        
    # Replace the targets array
    # Look for const targets = [...];
    new_targets_json = json.dumps(valid_targets, ensure_ascii=False, indent=4)
    
    # Regex replacement
    pattern = r'const targets = \[.*?\];'
    replacement = f'const targets = {new_targets_json};'
    
    new_html = re.sub(pattern, replacement, html, flags=re.DOTALL)
    
    # Also increase radius to 300
    new_html = new_html.replace('rvClient.getNearestPanoId(position, 50,', 'rvClient.getNearestPanoId(position, 300,')
    
    with open('auto_pov_pilot.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
        
    print("Updated HTML with valid targets and radius 300.")

if __name__ == "__main__":
    update_html()
