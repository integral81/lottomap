import requests
import re
import json

x, y = 127.3254, 37.35558
headers = {
    'Referer': 'https://map.kakao.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    r = requests.get(f'https://map.kakao.com/roadview/metadata?x={x}&y={y}', headers=headers, timeout=5)
    if r.status_code == 200:
        content = r.text
        # Save to file safely
        with open('final_pano_meta.html', 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Search for panoId
        match = re.search(r'"panoId":(\d+)', content)
        if not match:
            match = re.search(r'"panoId":"([^"]+)"', content)
        
        if match:
            print(f"RESULT:PANOID:{match.group(1)}")
        else:
            # Check for other patterns
            match = re.search(r'"id":(\d+)', content)
            if match:
                print(f"RESULT:PANOID:{match.group(1)}")
            else:
                print("RESULT:FAILED")
    else:
        print(f"RESULT:HTTP:{r.status_code}")
except Exception as e:
    print(f"RESULT:ERROR:{str(e)}")
