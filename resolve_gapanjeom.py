
import requests
import json
import re

def resolve_gapanjeom():
    place_id = "26506631"
    # Check API first for exact coords
    url_search = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {"Authorization": "KakaoAK 84b62e85ed3ec32fca558717eda26006"}
    
    print(f"Resolving Gapanjeom ID {place_id}...")
    
    coords = None
    
    try:
        # Search by query "가판점" to find which doc matches ID?
        # Or just trust the mobile page trick again which worked well?
        # Official API doesn't allow Lookup by ID directly (unless using specific endpoint not standard)
        # But we can search for the specific name or address from the link context if we knew it?
        # User said "신도림역 2번출구".
        
        # Let's try the internal API approach again as it gave coordinates last time even if 404 for some.
        # Wait, the previous internal API attempt failed unique to Golden.
        # Let's try Mobile Page scraping first, it's robust.
        
        url_m = f"https://place.map.kakao.com/m/{place_id}"
        r = requests.get(url_m, headers={
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1"
        })
        
        content = r.text
        
        # Extract PanoID
        m_pid = re.search(r'panoid=(\d+)', content)
        # Extract Coords
        # often in "map_kakao.png?MX=...&MY=..." (WCONGNAMUL)
        # or "display:block; ... latitude" ? No.
        
        # Look for JSON in the mobile page
        m_json = re.search(r'window\.PLACE_DETAIL\s*=\s*({.*?});', content, re.DOTALL)
        # Mobile often parses differently.
        
        # Let's try the API Search for "신도림역 2번출구 가판점" to get official Coords matching ID?
        r_api = requests.get(url_search, headers=headers, params={"query": "신도림역 2번출구 가판점"}, timeout=5)
        if r_api.status_code == 200:
            for doc in r_api.json()['documents']:
                if doc['id'] == place_id:
                     print(f"API MATCH! {doc['place_name']} ({doc['id']})")
                     coords = (doc['y'], doc['x'])
                     break
        
        if not coords:
             # Try search by "가판점" + "구로구" (Sindorim is Guro)
             r_api2 = requests.get(url_search, headers=headers, params={"query": "가판점", "rect": "126.88,37.50,126.90,37.52"}, timeout=5) # Sindorim area
             # Hard to filter by ID if list is long.
             pass
             
        # Result
        if m_pid:
            print(f"FOUND PanoID: {m_pid.group(1)}")
            update_data("가판점", "구로구", m_pid.group(1), coords)
        elif coords:
            print(f"FOUND Coords only: {coords}")
            update_data("가판점", "구로구", None, coords)
        else:
            print("Could not resolve details.")
            
    except Exception as e:
        print(f"Error: {e}")

def update_data(name_key, addr_key, pid, coords):
    json_path = 'lotto_data.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    for item in data:
        # Match Name AND Address content
        if name_key in item['n'] and addr_key in item['a']:
             print(f"Matched Record: {item['n']} ({item['a']})")
             
             if pid:
                 item['pov'] = {"id": str(pid), "pan": 0, "tilt": 0, "zoom": 0}
             
             if coords:
                 item['lat'] = float(coords[0])
                 item['lng'] = float(coords[1])
                 # item['a'] = "신도림역 2번출구" # Optional update
                 
             print("Updated JSON.")
             break
             
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    # HTML
    html_target = 'verify_gapan.html'
    lat = coords[0] if coords else 37.508
    lng = coords[1] if coords else 126.891
    
    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Verify Gapanjeom</title>
<script type="text/javascript" src="https://dapi.kakao.com/v2/maps/sdk.js?appkey=84b62e85ed3ec32fca558717eda26006&libraries=services,roadview"></script>
<style>html,body{{height:100%;margin:0}}</style>
</head><body><div id="roadview" style="width:100%;height:100%"></div>
<script>
var rv = new kakao.maps.Roadview(document.getElementById('roadview'));
var pos = new kakao.maps.LatLng({lat}, {lng});
rv.setPanoId({pid if pid else 'null'}, pos); 
// If pid null, use getNearestPanoId logic...
if (!{pid if pid else 'null'}) {{
    var client = new kakao.maps.RoadviewClient();
    client.getNearestPanoId(pos, 50, function(p) {{ rv.setPanoId(p, pos); }});
}}
</script></body></html>"""
    with open(html_target, 'w', encoding='utf-8') as f: f.write(html)
    print(f"Generated {html_target}")

if __name__ == "__main__":
    resolve_gapanjeom()
