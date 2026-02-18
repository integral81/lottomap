import json
import os

# Data to update
updates = [
    {
        "name": "굿모닝",
        "keywords": ["전남", "순천", "중앙로"],
        "pov": {
            "id": "1205033387",
            "pan": 90.0,
            "tilt": -3.0,
            "zoom": 0
        }
    },
    {
        "name": "풍향동복권나라",
        "keywords": ["광주", "북구", "풍향동"],
        "pov": {
            "id": "1204199726",
            "pan": 28.5,
            "tilt": -2.7,
            "zoom": 1
        }
    }
]

file_path = 'lotto_data.json'
html_path = 'verify_success_batch.html'

def update_json():
    print("Loading JSON...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return

    updated_count = 0
    
    for item in data:
        addr = item.get('a', '')
        name = item.get('n', '')
        
        for update in updates:
            # Check name and keywords in address
            if update['name'] == name and all(k in addr for k in update['keywords']):
                item['pov'] = update['pov']
                print(f"Updated: {name} ({addr}) - POV: {update['pov']}")
                updated_count += 1
                
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"JSON Update Complete. {updated_count} entries updated.")

def generate_html():
    print("Generating HTML...")
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>POV 등록 성공 검증: 굿모닝 & 풍향동복권나라</title>
    <style>
        body {{ font-family: 'Malgun Gothic', sans-serif; background-color: #f0f2f5; margin: 0; padding: 20px; }}
        h1 {{ text-align: center; color: #333; }}
        .header-desc {{ text-align: center; color: #666; margin-bottom: 30px; }}
        .container {{ display: flex; flex-wrap: wrap; justify-content: center; gap: 30px; }}
        .card {{ background: white; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); width: 45%; min-width: 450px; overflow: hidden; }}
        .header {{ background: #4a90e2; color: white; padding: 15px 20px; font-weight: bold; font-size: 1.3em; display: flex; justify-content: space-between; align-items: center; }}
        .info {{ padding: 15px 20px; font-size: 0.95em; color: #555; border-bottom: 1px solid #eee; background-color: #fafafa; }}
        .info strong {{ color: #333; }}
        .roadview {{ width: 100%; height: 500px; }}
        .success-badge {{ background: #2ecc71; color: white; padding: 5px 12px; border-radius: 20px; font-size: 0.7em; letter-spacing: 1px; text-transform: uppercase; }}
    </style>
    <script type="text/javascript" src="//dapi.kakao.com/v2/maps/sdk.js?appkey=84b62e85ed3ec32fca558717eda26006"></script>
</head>
<body>
    <h1>🎉 POV 등록 성공 검증 리포트 🎉</h1>
    <div class="header-desc">
        사용자가 제보한 정보(Pan/Tilt/Zoom)가 실제 로드뷰에서 어떻게 보이는지 확인합니다.
    </div>
    <div class="container">
"""
    
    for i, shop in enumerate(updates):
        div_id = f"roadview{i}"
        pov = shop['pov']
        html_content += f"""
        <div class="card">
            <div class="header">
                {shop['name']}
                <span class="success-badge">Verified</span>
            </div>
            <div class="info">
                <strong>PanoID:</strong> {pov['id']} <br>
                <strong>Setting:</strong> Pan {pov['pan']} / Tilt {pov['tilt']} / Zoom {pov['zoom']}
            </div>
            <div id="{div_id}" class="roadview"></div>
        </div>
        """
        
    html_content += """
    </div>
    <script>
    """
    
    for i, shop in enumerate(updates):
        div_id = f"roadview{i}"
        pov = shop['pov']
        html_content += f"""
        var roadviewContainer{i} = document.getElementById('{div_id}');
        var roadview{i} = new kakao.maps.Roadview(roadviewContainer{i});
        var roadviewClient{i} = new kakao.maps.RoadviewClient();
        
        // PanoID를 직접 사용하여 로드뷰를 띄웁니다.
        roadview{i}.setPanoId({pov['id']}, new kakao.maps.LatLng(0,0)); 
        
        // 로드뷰가 초기화된 후 시점을 이동합니다.
        kakao.maps.event.addListener(roadview{i}, 'init', function() {{
            roadview{i}.setViewpoint({{
                pan: {pov['pan']},
                tilt: {pov['tilt']},
                zoom: {pov['zoom']}
            }});
        }});
        """
        
    html_content += """
    </script>
</body>
</html>
"""
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"HTML Generated: {os.path.abspath(html_path)}")

if __name__ == "__main__":
    update_json()
    generate_html()
