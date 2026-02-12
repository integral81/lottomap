import requests
import re

coords = [
    (127.325400, 37.355580),
    (127.325405, 37.355600),
    (127.325500, 37.355750)
]

headers = {
    'Referer': 'https://map.kakao.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

for x, y in coords:
    url = f'https://map.kakao.com/roadview/metadata?x={x}&y={y}'
    try:
        r = requests.get(url, headers=headers, timeout=5)
        if r.status_code == 200:
            content = r.text
            match = re.search(r'"panoId":(\d+)', content)
            if not match:
                match = re.search(r'"panoId":"([^"]+)"', content)
            
            if match:
                print(f"Success for ({x}, {y}): PanoID = {match.group(1)}")
                # Optional: print snippet
                # print(content[:500])
                break
            else:
                print(f"No PanoID found in metadata for ({x}, {y})")
        else:
            print(f"Failed for ({x}, {y}): Status {r.status_code}")
    except Exception as e:
        print(f"Error for ({x}, {y}): {e}")
