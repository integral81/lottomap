
import requests
import json

API_KEY = "84b62e85ed3ec32fca558717eda26006"

def resolve_gapan_final():
    target_id = "26506631"
    target_addr = "서울 구로구 새말로 117-21" # From local data match
    
    print(f"Resolving Gapanjeom (Target ID: {target_id})...")
    
    headers = {"Authorization": f"KakaoAK {API_KEY}"}
    
    # 1. Search by Keyword "가판점" near Sindorim
    # Sindorim Coords: 37.5088, 126.8912
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    params = {
        "query": "가판점",
        "y": "37.5088", "x": "126.8912",
        "radius": "200"
    }
    
    best_coords = None
    
    try:
        r = requests.get(url, headers=headers, params=params, timeout=5)
        if r.status_code == 200:
            docs = r.json()['documents']
            for doc in docs:
                print(f"Found: {doc['place_name']} (ID: {doc['id']})")
                if doc['id'] == target_id:
                    print("  -> MATCHED ID!")
                    best_coords = (doc['y'], doc['x'])
                    break
                    
        # 2. If no ID match, Search by Specific Address
        if not best_coords:
            print("Searching by Address...")
            url_addr = "https://dapi.kakao.com/v2/local/search/address.json"
            r2 = requests.get(url_addr, headers=headers, params={"query": target_addr}, timeout=5)
            if r2.status_code == 200:
                 docs = r2.json()['documents']
                 if docs:
                     best_coords = (docs[0]['y'], docs[0]['x'])
                     print(f"  -> Found Coords via Address: {best_coords}")
                     
        # 3. Apply Update
        if best_coords:
            update_gapan_json(best_coords[0], best_coords[1])
            generate_html(best_coords[0], best_coords[1])
        else:
            print("Could not resolve coordinates.")

    except Exception as e:
        print(f"Error: {e}")

def update_gapan_json(lat, lng):
    json_path = 'lotto_data.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    updated = False
    for item in data:
        # Match "가판점" and "구로구" (or key part of address)
        if "가판점" in item['n'] and "구로" in item['a']:
            item['lat'] = float(lat)
            item['lng'] = float(lng)
            # Clear invalid POV if any, or set dummy to enable scanner?
            # User wants "POV 등록". If we don't have ID, we can't register POV ID.
            # But we can register the coordinates so the scanner finds it.
            # OR we can try to guess PanoID from coords? No.
            # We set POV to null so verify_recovery_all checks it?
            # Or we set a "DYNAMIC" type in verify list.
            
            # Let's keep POV as is (or null) and rely on the HTML to show Roadview.
            if not item.get('pov'):
                 item['pov'] = None # Ensure it's explicitly null/reset if needed
                 
            print(f"Updated JSON coods for {item['n']}")
            updated = True
            break
            
    if updated:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
    # Update verify_recovery_all.html for this specific shop
    update_verify_list(float(lat), float(lng))

def update_verify_list(lat, lng):
    # We'll just patch the verify_recovery_all.html specifically for Gapanjeom
    pass

def generate_html(lat, lng):
    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Gapanjeom Verified</title>
<script type="text/javascript" src="https://dapi.kakao.com/v2/maps/sdk.js?appkey={API_KEY}&libraries=services,roadview"></script>
<style>html,body{{height:100%;margin:0}}</style>
</head><body><div id="roadview" style="width:100%;height:100%"></div>
<script>
var rv = new kakao.maps.Roadview(document.getElementById('roadview'));
var client = new kakao.maps.RoadviewClient();
var pos = new kakao.maps.LatLng({lat}, {lng});

// Auto-find nearest
client.getNearestPanoId(pos, 50, function(panoId) {{
    if(panoId) {{
        rv.setPanoId(panoId, pos);
        console.log("Found PanoID: " + panoId);
        // Show info
        var div = document.createElement('div');
        div.style.position = 'absolute'; div.style.top='10px'; div.style.left='10px';
        div.style.background='white'; div.style.padding='5px'; div.style.zIndex='999';
        div.innerHTML = 'PanoID: ' + panoId;
        document.body.appendChild(div);
    }} else {{
        alert('Roadview not found near ' + {lat} + ',' + {lng});
    }}
}});
</script></body></html>"""
    with open('verify_gapan.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Generated verify_gapan.html")

if __name__ == "__main__":
    resolve_gapan_final()
