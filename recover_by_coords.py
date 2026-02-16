
import re
import json

def recover_by_coords():
    fname = 'commit_42_povs_utf8.txt'
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Targets with (lat, lng) approximate
    targets = [
        {"n": "Golden Lottery", "lat": 35.155, "lng": 129.039},
        {"n": "Lottery Masterpiece", "lat": 35.851, "lng": 128.616},
        {"n": "Gapanjeom 2", "lat": 37.50, "lng": 126.89},
        {"n": "Mokhwa", "lat": 35.00, "lng": 128.05}, 
    ]
    
    found_data = []
    
    # Split into potential blocks
    # Looking for { ... }
    # A bit hacky: split by "{" and verify content
    
    parts = content.split('{')
    for part in parts:
        # Reconstruct roughly
        block = "{" + part
        # Check if it contains lat/lng keys
        if '"lat":' in block and '"lng":' in block:
            # Extract numbers
            try:
                lat_m = re.search(r'"lat":\s*([0-9\.]+)', block)
                lng_m = re.search(r'"lng":\s*([0-9\.]+)', block)
                
                if lat_m and lng_m:
                    lat = float(lat_m.group(1))
                    lng = float(lng_m.group(1))
                    
                    # Check against targets
                    for t in targets:
                        if abs(lat - t['lat']) < 0.01 and abs(lng - t['lng']) < 0.01:
                            print(f"--- MATCH: {t['n']} ---")
                            # Try to extract the full object
                            end_brace = block.find('}')
                            if end_brace != -1:
                                snippet = block[:end_brace+1]
                                # Clean git diff markers
                                snippet = re.sub(r'\n[\+\-]', '\n', snippet)
                                print(snippet)
                                found_data.append(snippet)
            except:
                pass

    with open('recovered_by_coords.json', 'w', encoding='utf-8') as f:
        json.dump(found_data, f, indent=2)

if __name__ == "__main__":
    recover_by_coords()
