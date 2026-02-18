import requests
import json
import re
from urllib.parse import urlparse, parse_qs

def main():
    # 1. Expand URL
    short_url = "https://kko.to/ZSr2P4edqF"
    try:
        r = requests.get(short_url, allow_redirects=True)
        full_url = r.url
        print(f"Full URL: {full_url}")
        
        # 2. Extract Params
        # Typical format: https://map.kakao.com/?...&panoid=...&pan=...&tilt=...&zoom=...
        parsed = urlparse(full_url)
        params = parse_qs(parsed.query)
        
        panoid = params.get('panoid', [None])[0]
        pan = params.get('pan', [None])[0]
        tilt = params.get('tilt', [None])[0]
        zoom = params.get('zoom', [None])[0]
        
        if not panoid:
            # Fallback for "roadviewId" or similar
            panoid = params.get('roadviewId', [None])[0]

        print(f"Extracted: panoid={panoid}, pan={pan}, tilt={tilt}, zoom={zoom}")
        
        if not panoid:
            print("Failed to extract PanoID. Aborting update to avoid corruption.")
            return

        # 3. Update JSON
        f_json = 'lotto_data.json'
        f_js = 'lotto_data.js'
        
        with open(f_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        updated = False
        target_name = "훼미리로또"
        
        for s in data:
            if target_name in s.get('n', ''):
                # Update POV
                s['panoid'] = int(panoid) if panoid.isdigit() else panoid
                s['pov'] = {
                    "pan": float(pan) if pan else 0.0,
                    "tilt": float(tilt) if tilt else 0.0,
                    "zoom": int(zoom) if zoom else 0
                }
                # Add Message
                s['roadview_msg'] = "훼미리마트는 CU보라매타운점으로 변경!!"
                
                print(f"Updated {s['n']} with new POV and Message.")
                updated = True
                break
        
        if updated:
            with open(f_json, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            with open(f_js, 'w', encoding='utf-8') as f:
                f.write('const lottoData = ' + json.dumps(data, ensure_ascii=False) + ';')
            print("Successfully saved data.")
        else:
            print(f"Shop '{target_name}' not found.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
