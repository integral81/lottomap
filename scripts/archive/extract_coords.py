import urllib.parse

url = 'https://map.kakao.com/?map_type=TYPE_MAP&map_attribute=ROADVIEW&panoid=1197820708&pan=333.6&tilt=-4.1&zoom=1&urlLevel=3&urlX=522391&urlY=1115084&q=%EC%9E%A0%EC%8B%A4%EB%A7%A4%EC%A0%90&hId=26506729&mode=place'

params = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)

# Kakao Map uses WCONGNAMUL coordinates, need to convert to WGS84
urlX = float(params['urlX'][0])
urlY = float(params['urlY'][0])

# Conversion formula (approximate)
# WGS84 = WCONGNAMUL coordinates need proper conversion
# For now, extract from the URL parameters
print(f"urlX (WCONGNAMUL): {urlX}")
print(f"urlY (WCONGNAMUL): {urlY}")

# The actual lat/lng should be extracted from the place info
# Let's use the coordinates from the roadview position
import requests

# Get the actual coordinates from Kakao API
response = requests.get(f'https://map.kakao.com/link/map/26506729')
print(response.url)
