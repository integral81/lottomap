
import requests

url = "https://kko.to/R6OMAMzaaF"

try:
    response = requests.get(url, allow_redirects=True, timeout=10)
    final_url = response.url
    print(f"Final URL: {final_url}")
    
    # Extract panoId and other parameters from URL
    if 'map.kakao.com' in final_url:
        print("\nParsing Kakao Map URL...")
        # URL format: https://map.kakao.com/?map_type=TYPE&target=roadview&...
        # We need to extract panoid, pan, tilt, zoom from the URL
        
        from urllib.parse import urlparse, parse_qs
        parsed = urlparse(final_url)
        params = parse_qs(parsed.query)
        
        print(f"\nURL Parameters:")
        for key, value in params.items():
            print(f"  {key}: {value}")
            
except Exception as e:
    print(f"Error: {e}")
