import json

def create_direct_links():
    target_shops = ["굿모닝", "풍향동복권나라", "현진식품"]
    found_data = []

    try:
        with open('lotto_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        for item in data:
            name = item.get('n', '')
            addr = item.get('a', '')
            
            # Simple keyword matching
            for target in target_shops:
                if target in name:
                    # Specific checks for ambiguity
                    if target == "굿모닝" and "순천" not in addr: continue
                    if target == "현진식품" and "구로" not in addr: continue
                    
                    found_data.append(item)
                    break
        
        # HTML Generation
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Direct Roadview Links</title>
            <style>
                body { font-family: 'Malgun Gothic', sans-serif; padding: 40px; background: #f0f2f5; text-align: center; }
                .card { background: white; border-radius: 12px; padding: 30px; margin: 20px auto; max-width: 600px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
                h2 { margin-top: 0; color: #333; }
                p { color: #666; margin-bottom: 20px; }
                .btn { display: inline-block; padding: 15px 30px; background: #fae100; color: #3c1e1e; text-decoration: none; font-weight: bold; border-radius: 8px; transition: 0.2s; }
                .btn:hover { background: #ffd200; transform: translateY(-2px); }
                .coord-link { display: block; margin-top: 10px; font-size: 0.9em; color: #888; text-decoration: none; }
            </style>
        </head>
        <body>
            <h1>🚀 Kakao Map Direct Links</h1>
            <p>보안 문제 없이 공식 카카오맵으로 연결됩니다.</p>
        """
        
        for shop in found_data:
            name = shop['n']
            addr = shop['a']
            lat = shop.get('lat', 0)
            lng = shop.get('lng', 0)
            pov = shop.get('pov', {})
            panoid = pov.get('id', '')
            
            # Construct URL
            # Priority: PanoID -> Lat/Lng
            if panoid:
                url = f"https://map.kakao.com/link/roadview/{panoid}"
                desc = f"PanoID: {panoid}"
            else:
                url = f"https://map.kakao.com/link/map/{name},{lat},{lng}" 
                desc = "좌표 기반 (로드뷰 미등록)"

            html += f"""
            <div class="card">
                <h2>{name}</h2>
                <p>{addr}</p>
                <a href="{url}" target="_blank" class="btn">로드뷰 열기 (새창)</a>
                <div style="margin-top:10px; font-size:0.8em; color:#999;">{desc}</div>
            </div>
            """
            
        html += "</body></html>"
        
        with open('verify_direct_links.html', 'w', encoding='utf-8') as f:
            f.write(html)
            print("Generated verify_direct_links.html")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_direct_links()
