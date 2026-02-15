
import json

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        lotto_data = json.load(f)
        
    shop_stats = {} 
    for item in lotto_data:
        addr = item.get('a', '').strip()
        name = item.get('n', '').strip()
        if not addr: continue
        
        if addr not in shop_stats:
            shop_stats[addr] = {
                "name": name, 
                "wins": 0, 
                "has_pov": False,
                "lat": item.get('lat'),
                "lng": item.get('lng'),
                "has_coords": item.get('lat') is not None
            }
        shop_stats[addr]["wins"] += 1
        if 'pov' in item:
            shop_stats[addr]["has_pov"] = True

    # Final list criteria: Exactly 4 wins and no POV
    missing_pov_shops = []
    for addr, info in shop_stats.items():
        if info['wins'] == 4 and not info['has_pov']:
            missing_pov_shops.append({
                "name": info['name'],
                "address": addr,
                "wins": info['wins'],
                "lat": info['lat'],
                "lng": info['lng'],
                "has_coords": info['has_coords']
            })
            
    # Sort by name
    missing_pov_shops.sort(key=lambda x: x['name'])
    
    js_shops = json.dumps(missing_pov_shops, ensure_ascii=False, indent=4)

    # Full functional script
    script_content = f"""
    <script>
        let map, rv, rvClient, marker;
        let currentShop = null;
        let accumulatedCodes = JSON.parse(localStorage.getItem('pov_accumulated_codes') || '[]');
        let allMissingShops = {js_shops};
        let registeredKeys = JSON.parse(localStorage.getItem('pov_registered_shops') || '[]');

        document.addEventListener('DOMContentLoaded', init);

        async function init() {{
            try {{
                if (typeof kakao !== 'undefined' && kakao.maps) {{
                    const mapContainer = document.getElementById('map');
                    const mapOption = {{ center: new kakao.maps.LatLng(37.4815, 127.0145), level: 3 }};
                    map = new kakao.maps.Map(mapContainer, mapOption);

                    const rvContainer = document.getElementById('roadview');
                    rv = new kakao.maps.Roadview(rvContainer);
                    rvClient = new kakao.maps.RoadviewClient();

                    marker = new kakao.maps.Marker({{
                        position: map.getCenter(),
                        map: map,
                        draggable: true
                    }});

                    kakao.maps.event.addListener(rv, 'init', updatePOVUI);
                    kakao.maps.event.addListener(rv, 'viewpoint_changed', updatePOVUI);
                    kakao.maps.event.addListener(rv, 'position_changed', updatePOVUI);

                    kakao.maps.event.addListener(marker, 'dragend', function () {{
                        const pos = marker.getPosition();
                        loadRoadview(pos.getLat(), pos.getLng());
                    }});
                }} else {{
                    document.getElementById('status-text').innerText = '지도 SDK 로드 실패';
                }}
            }} catch (err) {{
                console.error('Error during init:', err);
            }}
            renderShopList();
        }}

        function renderShopList() {{
            const filteredList = allMissingShops.filter(shop => {{
                const key = `${{shop.name}}|${{shop.address}}`;
                return !registeredKeys.includes(key);
            }});

            document.getElementById('missing-count').innerText = filteredList.length;
            document.getElementById('status-text').innerText = `남은 대상: ${{filteredList.length}}개`;

            const listContainer = document.getElementById('shop-list');
            listContainer.innerHTML = '';

            filteredList.forEach((shop, index) => {{
                const div = document.createElement('div');
                div.className = 'shop-item';
                if (currentShop && currentShop.name === shop.name && currentShop.address === shop.address) {{
                    div.classList.add('active');
                }}
                div.onclick = () => selectShop(shop, div);

                const nameDiv = document.createElement('div');
                nameDiv.className = 'shop-name';
                nameDiv.innerText = shop.name;

                const addrDiv = document.createElement('div');
                addrDiv.className = 'shop-addr';
                addrDiv.innerHTML = `<span>${{shop.address}}</span>`;

                const copyBtn = document.createElement('button');
                copyBtn.className = 'addr-copy-btn';
                copyBtn.innerText = '복사';
                copyBtn.onclick = (e) => {{
                    e.stopPropagation();
                    copyToClipboard(shop.address);
                }};
                addrDiv.appendChild(copyBtn);

                const winDiv = document.createElement('div');
                winDiv.className = 'win-count';
                winDiv.innerText = `${{shop.wins}}회 당첨`;

                div.appendChild(nameDiv);
                div.appendChild(addrDiv);
                div.appendChild(winDiv);
                listContainer.appendChild(div);
            }});
        }}

        function selectShop(shop, element) {{
            document.querySelectorAll('.shop-item').forEach(el => el.classList.remove('active'));
            element.classList.add('active');
            currentShop = shop;

            const moveLatLon = new kakao.maps.LatLng(shop.lat, shop.lng);
            map.setCenter(moveLatLon);
            marker.setPosition(moveLatLon);
            loadRoadview(shop.lat, shop.lng);
        }}

        function loadRoadview(lat, lng) {{
            const position = new kakao.maps.LatLng(lat, lng);
            rvClient.getNearestPanoId(position, 100, function (panoId) {{
                if (panoId) {{
                    rv.setPanoId(panoId, position);
                }} else {{
                    alert('로드뷰 데이터가 없습니다.');
                }}
            }});
        }}

        function updatePOVUI() {{
            if (!rv.getPanoId()) return;
            updateCodeOutput();
        }}

        function updateCodeOutput() {{
            if (currentShop && rv.getPanoId()) {{
                const panoId = rv.getPanoId();
                const vp = rv.getViewpoint();
                const zoom = Math.floor(vp.zoom) || 0;
                const code = `{{ name: "${{currentShop.name}}", addr: "${{currentShop.address}}", panoid: ${{panoId}}, pov: {{ pan: ${{vp.pan.toFixed(2)}}, tilt: ${{vp.tilt.toFixed(2)}}, zoom: ${{zoom}} }} }},`;
                document.getElementById('current-code-text').textContent = code;
            }}
            
            document.getElementById('stack-output').textContent = accumulatedCodes.join('\\n');
            document.getElementById('stack-count').textContent = accumulatedCodes.length;
            const stackArea = document.getElementById('stack-area');
            stackArea.scrollTop = stackArea.scrollHeight;
        }}

        function copyStack() {{
            if (accumulatedCodes.length === 0) return;
            const text = accumulatedCodes.join('\\n');
            navigator.clipboard.writeText(text).then(() => {{
                showToast('전체 복사 완료!');
            }});
        }}

        function clearStack() {{
            if (confirm('누적 리스트를 비우시겠습니까?')) {{
                accumulatedCodes = [];
                localStorage.setItem('pov_accumulated_codes', '[]');
                updateCodeOutput();
            }}
        }}

        function markAsRegistered() {{
            if (!currentShop || !rv.getPanoId()) return;
            const code = document.getElementById('current-code-text').textContent;
            if (!accumulatedCodes.includes(code)) {{
                accumulatedCodes.push(code);
                localStorage.setItem('pov_accumulated_codes', JSON.stringify(accumulatedCodes));
            }}
            
            const key = `${{currentShop.name}}|${{currentShop.address}}`;
            if (!registeredKeys.includes(key)) {{
                registeredKeys.push(key);
                localStorage.setItem('pov_registered_shops', JSON.stringify(registeredKeys));
            }}
            
            showToast('추가되었습니다.');
            renderShopList();
            updateCodeOutput();
        }}

        function resetRegistered() {{
            if (confirm('등록 상태를 모두 초기화하시겠습니까?')) {{
                localStorage.removeItem('pov_registered_shops');
                registeredKeys = [];
                renderShopList();
            }}
        }}

        function copyToClipboard(text) {{
            navigator.clipboard.writeText(text).then(() => showToast('복사되었습니다.'));
        }}

        function showToast(msg) {{
            const toast = document.createElement('div');
            toast.innerText = msg;
            toast.style.cssText = 'position:fixed; bottom:20px; left:50%; transform:translateX(-50%); background:rgba(0,0,0,0.8); color:white; padding:8px 16px; border-radius:20px; font-size:13px; z-index:9999;';
            document.body.appendChild(toast);
            setTimeout(() => toast.remove(), 1500);
        }}

        function exportRegistered() {{
            const data = localStorage.getItem('pov_registered_shops');
            const newWindow = window.open('', '_blank');
            newWindow.document.write('<textarea style="width:100%;height:100%;">' + data + '</textarea>');
        }}
    </script>
    """

    with open('admin_pov.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    script_start = html.find('<script>')
    if script_start != -1:
        new_html = html[:script_start] + script_content + "</body></html>"
        with open('admin_pov.html', 'w', encoding='utf-8') as f:
            f.write(new_html)
        print("✅ FULL RECOVERY SUCCESS")
    else:
        print("❌ FAILED TO FIND SCRIPT TAG")

except Exception as e:
    print(f"Error: {e}")
