import requests
import re
import time

# Target coordinate (building)
start_x, start_y = 127.32540015887, 37.3555798712105

# Sweep a grid around the target to find a road point
# Gyeongchung-daero is a major road, should have roadview points
offsets = []
for i in range(-5, 6):
    for j in range(-5, 6):
        offsets.append((i * 0.0002, j * 0.0002))

headers = {
    'Referer': 'https://map.kakao.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

found_pano = None
for dx, dy in offsets:
    x, y = start_x + dx, start_y + dy
    url = f'https://map.kakao.com/roadview/metadata?x={x}&y={y}'
    try:
        r = requests.get(url, headers=headers, timeout=2)
        if r.status_code == 200:
            content = r.text
            match = re.search(r'"panoId":(\d+)', content)
            if not match:
                match = re.search(r'"panoId":"([^"]+)"', content)
            
            if match:
                pano_id = match.group(1)
                print(f"FOUND PanoID: {pano_id} at ({x}, {y})")
                found_pano = pano_id
                break
    except:
        pass
    time.sleep(0.1)

if not found_pano:
    print("Failed to find any PanoID in the grid.")
else:
    # Get details of the found pano
    print(f"SUCCESS: {found_pano}")
