
import json

def apply_lotto_rest_url():
    # Resolved Data
    new_data = {
        "name": "로또휴게실",
        "addr": "경기 용인시 기흥구 용구대로 1885", 
        "panoId": 1199447820,
        "pov": { "pan": 282.0, "tilt": 1.2, "zoom": 0 } # Using Zoom 0 as default
    }
    
    # 1. Update lotto_data.json
    json_path = 'lotto_data.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    updated = False
    for item in data:
        if "로또휴게실" in item['n']:
            item['pov'] = new_data['pov']
            item['pov']['id'] = str(new_data['panoId']) # Ensure string ID in data
            # Also update address to match verified URL?
            # URL q-param: 경기 용인시 기흥구 용구대로 1885
            item['a'] = new_data['addr']
            updated = True
            print("Updated '로또휴게실' in lotto_data.json")
            break
            
    if updated:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
    # 2. Generate HTML
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Verification: Lotto Rest Area</title>
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
        <h3>로또휴게실 (User Verified URL)</h3>
        <p>Addr: {new_data['addr']}</p>
        <p>PanoID: {new_data['panoId']}</p>
        <p>POV: Pan {new_data['pov']['pan']}, Tilt {new_data['pov']['tilt']}</p>
    </div>
    <div id="roadview"></div>
    <script>
        var rvContainer = document.getElementById('roadview');
        var roadview = new kakao.maps.Roadview(rvContainer);
        var panoId = {new_data['panoId']};
        var pov = {{ pan: {new_data['pov']['pan']}, tilt: {new_data['pov']['tilt']}, zoom: 0 }};
        
        roadview.setPanoId(panoId, new kakao.maps.LatLng(37.256, 127.104)); // Dummy coord
        
        kakao.maps.event.addListener(roadview, 'init', function() {{
            roadview.setViewpoint(pov);
        }});
    </script>
</body>
</html>"""

    with open('verify_lotto_rest.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Generated verify_lotto_rest.html")

if __name__ == "__main__":
    apply_lotto_rest_url()
