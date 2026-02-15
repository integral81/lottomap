import requests
import re
import json

def register_heungyang():
    # 1. Resolve URL again to get Pano ID (didn't capture it in previous step easily)
    short_url = "https://kko.to/wuUavtCqeJ"
    try:
        response = requests.get(short_url, allow_redirects=True)
        final_url = response.url
        print(f"Final URL: {final_url}")
        
        # Extract POV
        # Example: https://map.kakao.com/?map_type=TYPE_MAP&map_attribute=ROADVIEW&panoid=1195679262&pan=99.0&tilt=0.0&zoom=0...
        pano_match = re.search(r'panoid=(\d+)', final_url)
        pan_match = re.search(r'pan=([\d.-]+)', final_url)
        tilt_match = re.search(r'tilt=([\d.-]+)', final_url)
        zoom_match = re.search(r'zoom=([\d.-]+)', final_url)
        
        if pano_match:
            pov_data = {
                "id": pano_match.group(1),
                "pan": float(pan_match.group(1)) if pan_match else 0.0,
                "tilt": float(tilt_match.group(1)) if tilt_match else 0.0,
                "zoom": int(float(zoom_match.group(1))) if zoom_match else 0
            }
            print(f"Extracted POV: {pov_data}")
            
            # 2. Update JSON
            json_path = 'lotto_data.json'
            target_name = "흥양마중물"
            target_addr = "강원 원주시 치악로 2335 (소초면 흥양리 1718-4)"
            target_lat = 37.383692
            target_lng = 127.975354
            
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            count = 0
            for item in data:
                # Match "흥양마중물"
                if "흥양마중물" in item.get('n', ''):
                    item['n'] = target_name
                    item['a'] = target_addr
                    item['lat'] = target_lat
                    item['lng'] = target_lng
                    item['pov'] = pov_data
                    if 'closed' in item:
                        del item['closed']
                    count += 1
                    
            if count > 0:
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"Successfully consolidated {count} records for {target_name}.")
            else:
                print("No matching records found.")
                
        else:
            print("Failed to extract Pano ID from URL.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    register_heungyang()
