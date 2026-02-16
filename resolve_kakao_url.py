
import requests
import re

def resolve_url():
    short_url = "https://kko.to/WbGsyCJaUg"
    print(f"Resolving {short_url}...")
    
    try:
        # Follow redirects
        r = requests.get(short_url, allow_redirects=True, timeout=10)
        final_url = r.url
        print(f"Final URL: {final_url}")
        
        # Check for Roadview ID (panoid)
        # URL often looks like: https://map.kakao.com/?...&panoid=12345...
        # or map_type=TYPE_SKYVIEW...
        
        pano_match = re.search(r'panoid=(\d+)', final_url)
        lat_match = re.search(r'map_point=([0-9\.]+),([0-9\.]+)', final_url) # Might be different param
        
        # Sometimes lat/lng are in q-param or just center
        # Let's inspect the URL structure
        
        # If it's a Place URL, we might need to fetch the place info. 
        # But 'kko.to' usually shares a specific view or place.
        
        # Parse logic
        pano_id = pano_match.group(1) if pano_match else None
        
        # Try finding pan/tilt
        pan_match = re.search(r'pan=([0-9\.\-]+)', final_url)
        tilt_match = re.search(r'tilt=([0-9\.\-]+)', final_url)
        zoom_match = re.search(r'zoom=([0-9\.\-]+)', final_url)
        
        if pano_id:
            print(f"FOUND PanoID: {pano_id}")
            print(f"POV: pan={pan_match.group(1) if pan_match else '0'}, tilt={tilt_match.group(1) if tilt_match else '0'}")
        else:
            print("No PanoID found in URL.")
            
            # If it is a Place URL (e.g. place.map.kakao.com/ID), we can get coords
            # But roadview link is preferred.
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    resolve_url()
