
import requests
import re
import json

API_KEY = "84b62e85ed3ec32fca558717eda26006"

def check_alternatives():
    place_id = "2064777628"
    
    # 1. Search via API to verify ID and get coords
    print("Checking API for Place ID...")
    url_search = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {"Authorization": f"KakaoAK {API_KEY}"}
    
    found_coords = None
    
    try:
        # Search by name first
        r = requests.get(url_search, headers=headers, params={"query": "황금복권방"}, timeout=5)
        if r.status_code == 200:
            for doc in r.json()['documents']:
                if doc['id'] == place_id:
                    print(f"MATCH! Place ID {place_id} matches '{doc['place_name']}'")
                    print(f"Coords: {doc['y']}, {doc['x']}")
                    found_coords = (doc['y'], doc['x'])
                    break
        
        if not found_coords:
            # Search by specific address if name fails
            # But we don't know the address for sure? User said "Golden Lottery"
            pass
            
    except Exception as e:
        print(f"API Error: {e}")
        
    # 2. Check Mobile Page for PanoID
    print("\nChecking Mobile Page...")
    url_m = f"https://place.map.kakao.com/m/{place_id}"
    try:
        headers_m = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1"
        }
        r = requests.get(url_m, headers=headers_m, timeout=10)
        content = r.text
        
        # Regex for panoId
        # Look for "panoid" or "panoId"
        # Often in a link: href="...panoid=..."
        
        m = re.search(r'panoid=(\d+)', content)
        if m:
            print(f"FOUND PanoID in Mobile: {m.group(1)}")
            
            # Apply update!
            apply_golden_update(m.group(1), found_coords)
            return
            
        # Or look for "roadview" object
        if '"panoId"' in content:
             m2 = re.search(r'"panoId":"(\d+)"', content)
             if m2:
                 print(f"FOUND PanoID in Mobile JSON: {m2.group(1)}")
                 apply_golden_update(m2.group(1), found_coords)
                 return
                 
        print("PanoID not found in Mobile page.")
        
    except Exception as e:
        print(f"Mobile Error: {e}")

    # Fallback: Use Coords to generate Auto-Find HTML
    if found_coords:
        print("Using API Coordinates for Auto-Find...")
        update_golden_coords(float(found_coords[0]), float(found_coords[1]))

def apply_golden_update(pano_id, coords):
    # Update JSON with fixed PanoID
    json_path = 'lotto_data.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    for item in data:
        if "황금복권방" in item['n']:
            item['pov'] = {"id": str(pano_id), "pan": 0, "tilt": 0, "zoom": 0}
            if coords:
                item['lat'] = float(coords[0])
                item['lng'] = float(coords[1])
            print("Updated Golden Lottery with PanoID " + pano_id)
            break
            
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    # Generate HTML
    generate_html(pano_id)

def update_golden_coords(lat, lng):
    # Update JSON with coords only
    json_path = 'lotto_data.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    for item in data:
        if "황금복권방" in item['n']:
            item['lat'] = lat
            item['lng'] = lng
            # POV remains null or whatever so scanner/Auto-Find works
            print(f"Updated Golden Lottery with Coords {lat}, {lng}")
            break
            
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Generate Auto-Find HTML
    generate_html_auto(lat, lng)

def generate_html(pano_id):
    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Golden Verified</title>
<script type="text/javascript" src="https://dapi.kakao.com/v2/maps/sdk.js?appkey={API_KEY}&libraries=services,roadview"></script>
<style>html,body{{height:100%;margin:0}}</style>
</head><body><div id="roadview" style="width:100%;height:100%"></div>
<script>
var roadview = new kakao.maps.Roadview(document.getElementById('roadview'));
roadview.setPanoId({pano_id}, new kakao.maps.LatLng(35, 129));
</script></body></html>"""
    with open('verify_golden.html', 'w', encoding='utf-8') as f: f.write(html)

def generate_html_auto(lat, lng):
    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Golden Auto-Find</title>
<script type="text/javascript" src="https://dapi.kakao.com/v2/maps/sdk.js?appkey={API_KEY}&libraries=services,roadview"></script>
<style>html,body{{height:100%;margin:0}}</style>
</head><body><div id="roadview" style="width:100%;height:100%"></div>
<script>
var rv = new kakao.maps.Roadview(document.getElementById('roadview'));
var client = new kakao.maps.RoadviewClient();
var pos = new kakao.maps.LatLng({lat}, {lng});
client.getNearestPanoId(pos, 50, function(panoId) {{
    if(panoId) rv.setPanoId(panoId, pos);
    else alert('Roadview not found near ' + {lat} + ',' + {lng});
}});
</script></body></html>"""
    with open('verify_golden.html', 'w', encoding='utf-8') as f: f.write(html)

if __name__ == "__main__":
    check_alternatives()
