
import requests
from urllib.parse import urlparse, parse_qs
import json

url = "https://kko.to/fkVJ1y0vfs"

try:
    # 1. Resolve URL
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
        
        print(f"POV Data: panoid={panoid}, pan={pan}, tilt={tilt}, zoom={zoom}")
        
        # 2. Register to lotto_data.json
        target_name = "다모아복권"
        target_addr = "서울 구로구 오류동 315-14"
        
        pov_data = {
            "id": panoid,
            "pan": float(pan),
            "tilt": float(tilt),
            "fov": 40
        }
        
        with open('lotto_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        updated_count = 0
        for item in data:
            if target_name in item.get('n', '') and '오류동 315-14' in item.get('a', ''):
                item['pov'] = pov_data
                updated_count += 1
        
        if updated_count > 0:
            with open('lotto_data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Successfully updated {updated_count} entries for {target_name}.")
        else:
            print(f"No matching shop found for {target_name}.")
            
except Exception as e:
    print(f"Error: {e}")
