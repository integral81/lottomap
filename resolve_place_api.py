
import requests
import json
import re

def resolve_place_api():
    place_id = "2064777628"
    url = f"https://place.map.kakao.com/main/v/{place_id}"
    print(f"Fetching Internal API: {url}")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": f"https://place.map.kakao.com/{place_id}"
    }
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            data = r.json()
            # Check for roadview
            # Usually data['basicInfo']['roadview']
            
            basic = data.get('basicInfo', {})
            rv = basic.get('roadview', {})
            
            if rv:
                print(f"FOUND Roadview Data!")
                print(f"PanoID: {rv.get('panoid')}")
                print(f"POV: pan={rv.get('pan')}, tilt={rv.get('tilt')}, zoom={rv.get('zoom')}")
                
                # Also get coords
                print(f"Coords (WGS84?): {basic.get('wpointx')}, {basic.get('wpointy')}")
                
                # Update lotto_data.json
                if rv.get('panoid'):
                    update_golden(rv['panoid'], rv.get('pan', 0), rv.get('tilt', 0))
            else:
                print("No Roadview data in API response.")
                print(json.dumps(basic, indent=2, ensure_ascii=False)[:500])
        else:
             print(f"API Returned {r.status_code}")
             
    except Exception as e:
        print(f"Error: {e}")

def update_golden(pano_id, pan, tilt):
    json_path = 'lotto_data.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    updated = False
    for item in data:
        if "황금복권방" in item['n']:
            item['pov'] = {
                "id": str(pano_id),
                "pan": pan,
                "tilt": tilt,
                "zoom": 0
            }
            # Update address if needed?
            # Place API has address too.
            # let's trust the user's intent is just POV
            updated = True
            print("Updated '황금복권방' in lotto_data.json")
            break
            
    if updated:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
    # Also update HTML?
    # Generate a specific validation HTML for this shop
    generate_html(pano_id, pan, tilt)

def generate_html(pano_id, pan, tilt):
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Verification: Golden Lottery</title>
    <script type="text/javascript" src="https://dapi.kakao.com/v2/maps/sdk.js?appkey=a6b27b6dab16c7e3459bb9589bf1269d&libraries=services,roadview"></script>
    <style>
        body, html {{ width: 100%; height: 100%; margin: 0; }}
        #roadview {{ width: 100%; height: 100%; }}
        #info {{
            position: absolute; top: 10px; left: 10px; z-index: 999;
            background: white; padding: 10px; border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            font-family: sans-serif;
        }}
    </style>
</head>
<body>
    <div id="info">
        <h3>황금복권방 (User Verified URL)</h3>
        <p>PanoID: {pano_id}</p>
        <p>POV: Pan {pan}, Tilt {tilt}</p>
    </div>
    <div id="roadview"></div>
    <script>
        var rvContainer = document.getElementById('roadview');
        var roadview = new kakao.maps.Roadview(rvContainer);
        var panoId = {pano_id};
        var pov = {{ pan: {pan}, tilt: {tilt}, zoom: 0 }};
        
        roadview.setPanoId(panoId, new kakao.maps.LatLng(35.155, 129.039)); 
        
        kakao.maps.event.addListener(roadview, 'init', function() {{
            roadview.setViewpoint(pov);
        }});
    </script>
</body>
</html>"""
    with open('verify_golden.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Generated verify_golden.html")

if __name__ == "__main__":
    resolve_place_api()
