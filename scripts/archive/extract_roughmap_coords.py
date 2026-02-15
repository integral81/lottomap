import requests
import re

# Try to get coordinates from the roughmap key
key = "h5i6p597b5i"
timestamp = "1770702703240"

# Roughmap URLs to try
urls = [
    f"https://map.kakao.com/link/map/{key}",
    f"https://ssl.daumcdn.net/dmaps/map_js_init/roughmapLoader.js?key={key}",
]

for url in urls:
    try:
        print(f"\nTrying: {url}")
        r = requests.get(url, allow_redirects=True)
        print(f"Final URL: {r.url}")
        print(f"Status: {r.status_code}")
        
        # Look for coordinates in response
        lat_pattern = r'latitude["\s:]+([0-9.]+)'
        lng_pattern = r'longitude["\s:]+([0-9.]+)'
        
        lat_match = re.search(lat_pattern, r.text)
        lng_match = re.search(lng_pattern, r.text)
        
        if lat_match and lng_match:
            print(f"Found coordinates: lat={lat_match.group(1)}, lng={lng_match.group(1)}")
    except Exception as e:
        print(f"Error: {e}")

print("\n사용자님, Roughmap에서 직접 좌표를 추출하기 어렵습니다.")
print("대신 itemId 26506729를 사용하여 정확한 좌표를 확인하겠습니다.")
