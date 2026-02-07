import pandas as pd
import json

# [1단계] 데이터 불러오기 및 전처리
file_name = 'lotto_results_kinov_repaired.xlsx - Sheet1.csv'
df = pd.read_csv(file_name)

# Shorts 제작을 위해 상위 100개만 우선 시각화 (데이터가 너무 많으면 로딩이 느려짐)
sample_df = df[['상호명', '소재지']].head(100)
lotto_json = json.dumps(sample_df.to_dict('records'), ensure_ascii=False)

# [2단계] 카카오맵 시각화 코드(HTML/JS) 문자열 만들기
kakao_key = "b29ba13a6dceba9dda144cda55359e59"

html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>KINOV 로또 명당 지도 시각화</title>
    <style>
        #map {{ width: 100%; height: 95vh; margin: 0; padding: 0; }}
        body {{ margin: 0; }}
    </style>
</head>
<body>
    <div id="map"></div>
    <script src="//dapi.kakao.com/v2/maps/sdk.js?appkey={kakao_key}&libraries=services"></script>
    <script>
        var mapContainer = document.getElementById('map');
        var mapOption = {{ 
            center: new kakao.maps.LatLng(36.5, 127.5), 
            level: 12 
        }}; 
        var map = new kakao.maps.Map(mapContainer, mapOption);
        var geocoder = new kakao.maps.services.Geocoder();
        var locations = {lotto_json};

        locations.forEach(function(loc, index) {{
            // API 과부하 방지를 위해 0.1초 간격으로 순차적 지오코딩
            setTimeout(function() {{
                geocoder.addressSearch(loc.소재지, function(result, status) {{
                    if (status === kakao.maps.services.Status.OK) {{
                        var coords = new kakao.maps.LatLng(result[0].y, result[0].x);
                        var marker = new kakao.maps.Marker({{ 
                            map: map, 
                            position: coords 
                        }});
                        
                        var infowindow = new kakao.maps.InfoWindow({{
                            content: '<div style="padding:5px; font-size:12px; white-space:nowrap;">' + loc.상호명 + '</div>'
                        }});
                        
                        kakao.maps.event.addListener(marker, 'click', function() {{
                            infowindow.open(map, marker);
                        }});
                    }}
                }});
            }}, index * 100);
        }});
    </script>
</body>
</html>
"""

# [3단계] 결과 파일 저장하기
with open("lotto_map_kinov.html", "w", encoding="utf-8") as f:
    f.write(html_template)

print("---")
print("✅ 성공! 'lotto_map_kinov.html' 파일이 생성되었습니다.")
print("✅ 터미널에서 'python -m http.server 80' 실행 후")
print("✅ 브라우저에서 http://localhost/lotto_map_kinov.html 에 접속하세요.")
print("---")