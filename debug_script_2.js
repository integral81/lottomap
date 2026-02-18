
        function openOMR(numbers) {
            const grid = document.getElementById('omrGrid');
            grid.innerHTML = '';

            // Generate 1-45 grid
            for (let i = 1; i <= 45; i++) {
                const cell = document.createElement('div');
                cell.className = 'omr-number';
                cell.innerText = i;
                if (numbers.includes(i)) {
                    cell.className += ' marked';
                }
                grid.appendChild(cell);
            }

            const modal = document.getElementById('omrModal');
            modal.style.display = 'flex';
            setTimeout(() => modal.className += ' show', 10);

            // Update global last viewed numbers (Standard logic: "Last checked" means last opened/viewed)
            lastRecommendedNumbers = numbers;
            localStorage.setItem('lastLottoNumbers', JSON.stringify(numbers));
        }

        function closeOMR() {
            const modal = document.getElementById('omrModal');
            modal.className = 'omr-modal-overlay';
            setTimeout(() => modal.style.display = 'none', 300);
        }

        // Quick OMR View from Hamburger Menu
        function openLastOMR() {
            if (lastRecommendedNumbers && lastRecommendedNumbers.length === 6) {
                closeNav();
                openOMR(lastRecommendedNumbers);
            } else {
                // Show alert box in hamburger menu
                const alertBox = document.getElementById('omrAlertBox');
                alertBox.style.display = 'block';

                // Auto-hide after 4 seconds
                setTimeout(() => {
                    alertBox.style.display = 'none';
                }, 4000);
            }
        }

        // Updated Clipboard function (Global)
        // Note: Replaces/Overwrites the old one if names collide, or just exists as a better version
        window.copyToClipboard = function (numbers) {
            let text = "";
            if (Array.isArray(numbers)) {
                text = numbers.join(', ');
            } else {
                text = numbers;
            }

            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(text).then(() => {
                    showToast(`📋 번호가 복사되었습니다: ${text} `);
                }).catch(err => {
                    showToast('복사 실패: ' + err);
                });
            } else {
                // Fallback
                const textarea = document.createElement('textarea');
                textarea.value = text;
                document.body.appendChild(textarea);
                textarea.select();
                try {
                    document.execCommand('copy');
                    showToast("📋 번호가 복사되었습니다 (구형 브라우저)", "success");
                } catch (err) {
                    showToast("복사 실패", "error");
                }
                document.body.removeChild(textarea);
            }
        };

        // ============ Roadview Functions ============

        function openRoadview(arg1, arg2, arg3, arg4, arg5, arg6) {
            const roadviewContainer = document.getElementById('roadview-modal');
            const roadviewEl = document.getElementById('roadview');
            const imgContainer = document.getElementById('roadviewImageContainer');
            const helpText = document.getElementById('roadviewHelpText');
            const copyBtn = document.getElementById('roadviewCopyBtn');
            const naviBtn = document.getElementById('roadviewNaviBtn');

            let lat, lng, shopName, address, actionType, actionData, shop;

            // Handle Overloaded Arguments
            if (typeof arg1 === 'object' && arg1 !== null) {
                // Called with shop object: openRoadview(shop)
                shop = arg1;
                lat = shop.lat;
                lng = shop.lng;
                shopName = shop.n;
                address = shop.a;
                actionType = null;
                actionData = null;
            } else {
                // Called with individual args: openRoadview(lat, lng, name, addr, type, data)
                lat = arg1;
                lng = arg2;
                shopName = arg3;
                address = arg4;
                actionType = arg5;
                actionData = arg6;
                shop = { lat, lng, n: shopName, a: address }; // Mock shop object
            }

            // Lazy Initialization
            if (!roadview) {
                roadview = new kakao.maps.Roadview(roadviewEl);
            }
            if (!roadviewClient) {
                roadviewClient = new kakao.maps.RoadviewClient();
            }

            const staticImg = document.getElementById('roadviewStaticImage');

            // Resolve Preset
            // The original code had `if (preset && preset.imageUrl)` and `if (preset && preset.panoId)`.
            // This implies 'preset' was already defined or expected to be.
            // Let's define it here based on the shopName and address.
            // Assuming ROADVIEW_PRESETS is a global array.
            const foundPreset = ROADVIEW_PRESETS.find(p => p.name === shopName || (p.addr && address.includes(p.addr)));
            const activePreset = foundPreset || null;

            // Custom Message Sync
            const msgOverlay = document.getElementById('roadview-message-overlay');
            const shopMsgEl = document.getElementById('shop-message');

            if (msgOverlay) {
                // Priority: shop.customMessage > shop-message element content
                if (shop.customMessage) {
                    msgOverlay.textContent = shop.customMessage;
                    msgOverlay.style.display = 'block';
                } else if (shopMsgEl && shopMsgEl.textContent && shopMsgEl.style.display !== 'none') {
                    msgOverlay.textContent = shopMsgEl.textContent;
                    msgOverlay.style.display = 'block';
                } else {
                    msgOverlay.style.display = 'none';
                }
            }


            // Static Image Mode
            if (activePreset && activePreset.imageUrl) {
                // Display Static Image
                roadviewEl.style.display = 'none';
                imgContainer.style.display = 'block';
                staticImg.src = activePreset.imageUrl;
                helpText.style.display = 'none';
                roadviewContainer.style.display = 'block';

                // Action buttons setup for Image mode
                copyBtn.style.display = 'none';
                naviBtn.style.display = 'none';
                if (actionType === 'copy') {
                    copyBtn.style.display = 'inline-block';
                    copyBtn.onclick = () => { copyToClipboard(actionData); closeRoadview(); };
                } else if (actionType === 'navi') {
                    naviBtn.style.display = 'inline-block';
                    naviBtn.onclick = () => { openDirections(actionData.lat, actionData.lng, actionData.name); closeRoadview(); };
                }
                document.getElementById('roadviewKakaoMapBtn').onclick = () => openKakaoMap(lat, lng, shopName, address);
                return; // End here for image mode
            }

            // Normal Roadview Mode
            roadviewEl.style.display = 'block';
            imgContainer.style.display = 'none';
            helpText.style.display = 'block';

            const displayRoadview = (finalPanoId, finalPos) => {
                roadview.setPanoId(finalPanoId, finalPos);
                roadviewContainer.style.display = 'block';

                if (activePreset) {
                    setTimeout(() => {
                        roadview.setViewpoint(new kakao.maps.Viewpoint(activePreset.pov.pan, activePreset.pov.tilt, activePreset.pov.zoom));
                    }, 1200);
                }

                // Action buttons setup
                copyBtn.style.display = 'none';
                naviBtn.style.display = 'none';
                if (actionType === 'copy') {
                    copyBtn.style.display = 'inline-block';
                    copyBtn.onclick = () => { copyToClipboard(actionData); closeRoadview(); };
                } else if (actionType === 'navi') {
                    naviBtn.style.display = 'inline-block';
                    naviBtn.onclick = () => { openDirections(actionData.lat, actionData.lng, actionData.name); closeRoadview(); };
                }
                document.getElementById('roadviewKakaoMapBtn').onclick = () => openKakaoMap(lat, lng, shopName, address);
            };

            if (activePreset && activePreset.panoId) {
                // If we have a verified Pano ID, use it directly (bypass search)
                const verifiedPos = new kakao.maps.LatLng(lat, lng);
                displayRoadview(activePreset.panoId, verifiedPos);
            } else {
                // Precise Identification using Places Service
                const ps = new kakao.maps.services.Places();
                ps.keywordSearch(`${address} ${shopName} `, function (data, status) {
                    let targetPos = new kakao.maps.LatLng(lat, lng);
                    if (status === kakao.maps.services.Status.OK) {
                        const target = data.find(p => p.category_name.includes('복권') || p.place_name.includes(shopName)) || data[0];
                        targetPos = new kakao.maps.LatLng(target.y, target.x);
                    }
                    roadviewClient.getNearestPanoId(targetPos, 50, function (panoId) {
                        if (panoId === null) { alert('해당 점포는 로드뷰 정보가 없습니다.'); return; }
                        displayRoadview(panoId, targetPos);
                    });
                });
            }
        }

        function closeRoadview() {
            const modal = document.getElementById('roadview-modal');
            if (modal) modal.style.display = 'none';
        }

        function openRoadviewWithCopy(lat, lng, shopName, address) {
            openRoadview(lat, lng, shopName, address, 'copy', address);
        }

        function openRoadviewWithNavi(lat, lng, shopName, address) {
            if (shopName.includes('인터넷 복권판매사이트')) {
                window.open('https://www.dhlottery.co.kr/userGuide', '_blank');
                return;
            }
            openRoadview(lat, lng, shopName, address, 'navi', { lat, lng, name: shopName });
        }

        function openKakaoMap(lat, lng, shopName, address) {
            window.open(`https://map.kakao.com/?q=${encodeURIComponent(address + ' 복권')}`, '_blank');
        }

        function getDistance(lat1, lon1, lat2, lon2) {
            if ((lat1 == lat2) && (lon1 == lon2)) return 0;
            var radlat1 = Math.PI * lat1 / 180;
            var radlat2 = Math.PI * lat2 / 180;
            var theta = lon1 - lon2;
            var radtheta = Math.PI * theta / 180;
            var dist = Math.sin(radlat1) * Math.sin(radlat2) + Math.cos(radlat1) * Math.cos(radlat2) * Math.cos(radtheta);
            if (dist > 1) dist = 1;
            dist = Math.acos(dist);
            dist = dist * 180 / Math.PI;
            dist = dist * 60 * 1.1515;
            dist = dist * 1.609344; // km
            return dist;
        }
    