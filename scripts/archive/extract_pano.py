import re
try:
    with open('pano_meta.html', 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    match = re.search(r'"panoid":"([^"]+)"', content)
    if match:
        print(f"PanoID Found: {match.group(1)}")
    else:
        # Try a different regex pattern
        match = re.search(r'panoId\s*=\s*[\'"]([^\'"]+)[\'"]', content)
        if match:
            print(f"PanoID Found: {match.group(1)}")
        else:
            print("No PanoID found in metadata.")
except Exception as e:
    print(f"Error: {e}")
