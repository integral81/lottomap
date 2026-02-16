
import json

def register_gapan_final():
    """Register 종합가판점 (Sindorim) with final POV data"""
    
    target_name = "종합가판점"
    target_addr = "서울 구로구 가마산로"
    panoid = "1198164443"
    pov_data = {
        "id": panoid,
        "pan": 16.65,
        "tilt": 6.30,
        "zoom": 2
    }
    
    print(f"Registering {target_name} with PanoID {panoid}...")
    
    # Update lotto_data.json
    json_path = 'lotto_data.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    updated_count = 0
    for item in data:
        # Match by coordinates (Lat ~37.508, Lng ~126.891) to be precise
        if item.get('lat') and item.get('lng'):
            if 37.507 < item['lat'] < 37.509 and 126.890 < item['lng'] < 126.892:
                if "가판점" in item['n'] or "종합가판점" in item['n']:
                    # Update name (remove any prefix like ★(1순위))
                    item['n'] = target_name
                    item['a'] = target_addr
                    item['pov'] = pov_data
                    updated_count += 1
                    print(f"  Updated: {item['n']} | {item['a']}")
    
    if updated_count > 0:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\n[OK] Successfully updated {updated_count} entries in lotto_data.json")
    else:
        print("[WARN] No matching entries found")
        
    # Generate verification HTML
    generate_verification_html(panoid, pov_data)

def generate_verification_html(panoid, pov):
    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>종합가판점 (신도림) 검증</title>
<script type="text/javascript" src="https://dapi.kakao.com/v2/maps/sdk.js?appkey=84b62e85ed3ec32fca558717eda26006&libraries=services,roadview"></script>
<style>html,body{{height:100%;margin:0}}</style>
</head><body><div id="roadview" style="width:100%;height:100%"></div>
<script>
var rv = new kakao.maps.Roadview(document.getElementById('roadview'));
var pos = new kakao.maps.LatLng(37.5087701449787, 126.891080501385);
rv.setPanoId({panoid}, pos);
rv.setViewpoint({{pan: {pov['pan']}, tilt: {pov['tilt']}, zoom: {pov['zoom']}}});
</script></body></html>"""
    
    with open('verify_gapan_final.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("[OK] Generated verify_gapan_final.html")

if __name__ == "__main__":
    register_gapan_final()
