
import re

def search_coords_in_index():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Target Jamsil coords
    lat_target = 37.514
    lng_target = 127.101
    
    # Extract all objects from ROADVIEW_PRESETS or similar
    # In index.html, markers or presets are usually in a specific JS array
    match = re.search(r'const ROADVIEW_PRESETS = \[(.*?)\];', html, re.DOTALL)
    if not match:
        print("ROADVIEW_PRESETS not found")
        return
        
    content = match.group(1)
    objects = re.findall(r'\{(.*?)\}', content, re.DOTALL)
    
    found = []
    for obj in objects:
        # Check for panoId orimageUrl or customLink to see if it has visual info
        has_visual = "panoId" in obj or "imageUrl" in obj or "customLink" in obj
        
        # We need coordinates. Since presets usually DON'T have lat/lng directly (they use address),
        # but let's check anyway.
        # Actually, let's search for "신천동" or "올림픽로" or "잠실" in any registered item.
        if "잠실" in obj or "신천동" in obj or "올림픽로" in obj:
            found.append(obj.strip())
            
    if found:
        print(f"Found {len(found)} candidate(s) in index.html:")
        for i, f in enumerate(found):
            print(f"--- CANDIDATE {i+1} ---")
            print(f)
    else:
        print("No candidates found in index.html with Jamsil-related keywords.")

if __name__ == "__main__":
    search_coords_in_index()
