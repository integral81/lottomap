
import re

def get_gapanjeom_pano():
    fname = 'commit_42_povs_utf8.txt'
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Search for coordinates and finding the PanoID in the same block
    # Lat: 37.4939363498517
    
    idx = content.find("37.4939363498517")
    if idx != -1:
        print("Found Gapanjeom coordinates.")
        # Look backwards/forwards for "panoId"
        start = max(0, idx - 500)
        end = min(len(content), idx + 500)
        snippet = content[start:end]
        
        # Regex for PanoID
        m = re.search(r'"panoId":\s*(\d+)', snippet)
        if m:
            print(f"FOUND PanoID: {m.group(1)}")
        else:
            print("PanoID not found in snippet.")
            print(snippet)

if __name__ == "__main__":
    get_gapanjeom_pano()
