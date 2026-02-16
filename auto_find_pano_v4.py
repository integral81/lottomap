
import json
import requests
import math
import time
import os

def get_pano_id_from_coords(lat, lng):
    # Kakao internal endpoint (from find_pano_v3.py)
    # Note: This endpoint takes x, y which are lng, lat in standard terms?
    # x = lng, y = lat based on previous script usage.
    
    url = f'https://map.kakao.com/roadview/metadata?x={lng}&y={lat}'
    headers = {
        'Referer': 'https://map.kakao.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        r = requests.get(url, headers=headers, timeout=5)
        if r.status_code == 200:
            data = r.json()
            # The structure is usually data['panoId'] or similar
            # Let's inspect safety
            if 'panoId' in data:
                return data['panoId'], data.get('pan'), data.get('tilt')
            elif 'id' in data:
                return data['id'], data.get('pan'), data.get('tilt')
    except Exception as e:
        print(f"Error fetching pano metadata: {e}")
        
    return None, None, None

def calculate_bearing(lat1, lng1, lat2, lng2):
    # Calculate angle from Pano (lat2, lng2) to Shop (lat1, lng1)
    
    # Needs Pano Coords. 
    # Does metadata return Pano Coords? 
    # If not, we assume standard "facing road" or just use 0 (North).
    # The user accepted "Auto" - we can refine later.
    return 0 

def run_auto_recovery():
    print("--- [AUTO-RECOVERY V4] Using Internal API ---")
    
    try:
        with open('auto_pilot_candidates.json', 'r', encoding='utf-8') as f:
            targets = json.load(f)
            print(f"Loaded {len(targets)} candidates. Sample: {list(targets[0].keys())}")
    except:
        print("Candidates file missing. Regenerating defaults...")
        # (Fallback logic omitted for brevity, assuming file exists from previous step)
        return

    recovered = []
    
    for t in targets:
        if 'lat' not in t or 'lng' not in t:
            print(f"Skipping {t['n']} - No coordinates")
            continue
            
        print(f"Processing {t['n']} ({t['lat']}, {t['lng']})...")
        
        # Try finding Pano
        # We might need to spiral out if exact coord has no pano
        # But let's try exact first.
        
        pano_id, pan, tilt = get_pano_id_from_coords(t['lat'], t['lng'])
        
        if not pano_id:
            # Spiral search?
            # Let's try slight offsets (approx 10m)
            offsets = [
                (0.0001, 0), (-0.0001, 0), (0, 0.0001), (0, -0.0001)
            ]
            for dx, dy in offsets:
                pano_id, pan, tilt = get_pano_id_from_coords(t['lat'] + dx, t['lng'] + dy)
                if pano_id:
                    print(f"  Found with offset ({dx}, {dy})")
                    break
        
        if pano_id:
            print(f"  -> SUCCESS: ID {pano_id}")
            # Construct the recovered object
            # { name: "...", addr: "...", panoid: 123, pov: { pan: ..., tilt: ..., zoom: 0 }, lat:..., lng:... }
            
            rec = {
                "name": t['n'],
                "addr": t['a'],
                "panoid": int(pano_id),
                "pov": {
                    "pan": pan if pan else 0.0,
                    "tilt": tilt if tilt else 0.0,
                    "zoom": 0
                },
                "lat": t['lat'],
                "lng": t['lng']
            }
            recovered.append(rec)
        else:
            print("  -> FAILED to find PanoID.")
            
    if recovered:
        print(f"\nSuccessfully recovered {len(recovered)} shops!")
        with open('auto_recovery_results.json', 'w', encoding='utf-8') as f:
            json.dump(recovered, f, indent=2, ensure_ascii=False)
            
        # Format for user copy-paste
        print("\n=== COPY BELOW FOR CHAT ===")
        print(json.dumps(recovered, ensure_ascii=False))
        print("===========================")

if __name__ == "__main__":
    run_auto_recovery()
