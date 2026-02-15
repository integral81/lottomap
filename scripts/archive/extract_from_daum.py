import re

try:
    with open('daum_search_result.html', 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # 1. Look for panoId in various formats
    pano_ids = re.findall(r'panoid[:|=][\'"]?(\d{10})[\'"]?', content, re.I)
    print(f"PanoIDs found (regex 1): {list(set(pano_ids))}")
    
    # 2. Look for data-panoid
    pano_ids_alt = re.findall(r'data-panoid=[\'"]?(\d{10})[\'"]?', content)
    print(f"PanoIDs found (regex 2): {list(set(pano_ids_alt))}")
    
    # 3. Look for any 10-digit number that might be a panoId
    # Usually roadview panoIds are 10 digits starting with 10, 11, or 12
    potential_ids = re.findall(r'\b(1[012]\d{8})\b', content)
    print(f"Potential 10-digit IDs: {list(set(potential_ids))}")

except Exception as e:
    print(f"Error: {e}")
