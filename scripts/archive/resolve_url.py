
import requests
from urllib.parse import urlparse, parse_qs

url = "https://kko.to/_cukyu9908"

try:
    response = requests.get(url, allow_redirects=True, timeout=10)
    final_url = response.url
    print(f"Final URL: {final_url}")
    
    if 'map.kakao.com' in final_url:
        parsed = urlparse(final_url)
        params = parse_qs(parsed.query)
        
        panoid = params.get('panoid', [''])[0]
        pan = params.get('pan', [''])[0]
        tilt = params.get('tilt', [''])[0]
        zoom = params.get('zoom', [''])[0]
        
        print(f"\nExtracted POV Data:")
        print(f"  panoid: {panoid}")
        print(f"  pan: {pan}")
        print(f"  tilt: {tilt}")
        print(f"  zoom: {zoom}")
            
except Exception as e:
    print(f"Error: {e}")
