
import requests
import re
import json

def resolve_place_url():
    url = "https://place.map.kakao.com/2064777628"
    print(f"Resolving {url}...")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        content = r.text
        
        # Search for panoId in the source
        # Often inside `window.PLACE_DETAIL` or similar JSON structure
        
        # Pattern 1: "panoId":"12345"
        m = re.search(r'"panoId"\s*:\s*["\']?(\d+)["\']?', content)
        if m:
            print(f"FOUND PanoID (Pattern 1): {m.group(1)}")
            return m.group(1)
            
        # Pattern 2: "panoid" in some url inside
        m = re.search(r'panoid=(\d+)', content)
        if m:
            print(f"FOUND PanoID (Pattern 2): {m.group(1)}")
            return m.group(1)
            
        # Pattern 3: roadviewId
        m = re.search(r'"roadviewId"\s*:\s*["\']?(\d+)["\']?', content)
        if m:
             print(f"FOUND PanoID (Pattern 3): {m.group(1)}")
             return m.group(1)
             
        # Pattern 4: Look for coordinates and suggested lookup
        print("PanoID not directly found. Looking for coordinates...")
        
        # x, y (WCONGNAMUL)
        mx = re.search(r'"x"\s*:\s*(\d+)', content)
        my = re.search(r'"y"\s*:\s*(\d+)', content)
        
        if mx and my:
            print(f"Found WCoordinates: x={mx.group(1)}, y={my.group(1)}")
            # We can't easily convert WCONGNAMUL to WGS84 without API, 
            # but maybe we can use the `find_pano_v3.py` undocumented API with these?
            # url = f"https://map.kakao.com/roadview/metadata?x={x}&y={y}"
            return None, mx.group(1), my.group(1)

        print("Could not extract PanoID or Coords.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    resolve_place_url()
