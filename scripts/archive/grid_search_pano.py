import requests
import re

# Search around the target coordinates in a small grid
target_x, target_y = 127.3254, 37.35558
offsets = [0, 0.0001, -0.0001, 0.0002, -0.0002, 0.0003, -0.0003]

headers = {
    'Referer': 'https://map.kakao.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

found = False
for dx in offsets:
    if found: break
    for dy in offsets:
        x, y = target_x + dx, target_y + dy
        url = f'https://map.kakao.com/roadview/metadata?x={x}&y={y}'
        try:
            r = requests.get(url, headers=headers, timeout=3)
            if r.status_code == 200:
                content = r.text
                match = re.search(r'"panoId":(\d+)', content)
                if not match:
                    match = re.search(r'"panoId":"([^"]+)"', content)
                
                if match:
                    print(f"FOUND! Coord: ({x}, {y}) -> PanoID: {match.group(1)}")
                    found = True
                    break
        except:
            pass

if not found:
    print("Failed to find PanoID in the vicinity.")
