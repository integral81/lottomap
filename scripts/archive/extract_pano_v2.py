import re
try:
    with open('pano_meta_v2.html', 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    # Looking for panoId or similar
    match = re.search(r'"panoId":"([^"]+)"', content)
    if match:
        print(f"PanoID Found: {match.group(1)}")
    else:
        # Check for numeric panoId pattern
        match = re.search(r'"id":(\d+)', content)
        if match:
            print(f"PanoID Found: {match.group(1)}")
        else:
            # Maybe it's in a different case
            match = re.search(r'panoid":"([^"]+)"', content, re.I)
            if match:
                print(f"PanoID Found: {match.group(1)}")
            else:
                print("No PanoID found in metadata.")
except Exception as e:
    print(f"Error: {e}")
