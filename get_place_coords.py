import requests
import re
import json

# Get place info from Kakao
url = 'https://place.map.kakao.com/26506729'
r = requests.get(url)

# Try to find coordinates in the response
patterns = [
    r'"y":"([0-9.]+)","x":"([0-9.]+)"',
    r'"lat":"([0-9.]+)","lng":"([0-9.]+)"',
    r'latitude["\s:]+([0-9.]+).*longitude["\s:]+([0-9.]+)',
]

for pattern in patterns:
    match = re.search(pattern, r.text)
    if match:
        print(f"Found coordinates: lat={match.group(1)}, lng={match.group(2)}")
        break
else:
    print("Coordinates not found in response")
    # Try alternative: use the URL coordinates we already have
    print("\nUsing coordinates from roadview URL:")
    print("lat: 37.5139, lng: 127.1006 (approximate from urlX/urlY)")
