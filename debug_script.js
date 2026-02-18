
        let map;
        let clusterer;
        let allData = [];
        let markers = [];
        let currentInfoWindow = null; // Track the currently open InfoWindow
        let roadview = null; // Roadview instance
        let roadviewClient = null; // RoadviewClient instance

        // Premium Roadview POV Presets (User Verified 260210)
        const ROADVIEW_PRESETS = [
            // User Request: Sejin Electronics (Daegu)
            { name: "세진전자통신", addr: "대구 서구 서대구로", panoid: 1201585664, pov: { pan: 93.03, tilt: 5.09, zoom: -3 } },
            { name: "세방매점", addr: "경북 경주시 산업로", panoid: 1165999460, pov: { pan: 281.43, tilt: 6.82, zoom: -1 } },
            // User Request: 4 Recovered Shops (260216)
            { name: "대박행진 복권랜드", addr: "경기 파주시 금빛로", panoid: 1045548538, pov: { pan: 179.33, tilt: 3.10, zoom: -3 } },
            { name: "서울로또방", addr: "충북 옥천군 삼금로", panoid: 1185000546, pov: { pan: 206.53, tilt: 3.14, zoom: -3 } },
            { name: "우정식품", addr: "부산 동래구 온천장로", panoid: 1202699459, pov: { pan: 262.41, tilt: -2.15, zoom: -3 } },
            { name: "가로판매소", addr: "서울 구로구 새말로", panoid: 1198164443, pov: { pan: 17.40, tilt: 6.76, zoom: 2 } },
            { name: "원스탑", addr: "서울 송파구 백제고분로7길", panoid: 1197972914, pov: { pan: 27.06, tilt: -6.82, zoom: 0 } },
            // User Request: 18 Recovered Shops (260216-2)
            { name: "사이버정보통신", addr: "부산 부산진구 동평로", panoid: 1202364869, pov: { pan: 37.89, tilt: 2.99, zoom: -2 } },
            { name: "나눔로또편의점", addr: "전남 광양시 공영로", panoid: 1205201589, pov: { pan: 183.29, tilt: -2.32, zoom: -1 } },
            { name: "율암25시편의점", addr: "경기 화성시 시청로", panoid: 1198087972, pov: { pan: 158.58, tilt: 1.36, zoom: 0 } },
            { name: "해피+24시편의점", addr: "광주 북구 하서로", panoid: 1200291324, pov: { pan: 84.83, tilt: 1.48, zoom: -3 } },
            { name: "흥양마중물", addr: "강원 원주시 치악로", panoid: 1195199655, pov: { pan: 305.15, tilt: 13.98, zoom: -2 } },
            { name: "복권마트 & 씨스페이스 홍천점", addr: "강원 홍천군 홍천로", panoid: 1197150362, pov: { pan: 307.89, tilt: 2.54, zoom: -2 } },
            { name: "한국인세계대박복권", addr: "인천 연수구 독배로197번길", panoid: 1200648162, pov: { pan: 281.03, tilt: -2.90, zoom: -2 } },
            { name: "하이로또", addr: "서울 금천구 금하로", panoid: 1198115190, pov: { pan: 209.13, tilt: -1.64, zoom: -2 } },
            { name: "충남상회", addr: "인천 미추홀구 참외전로", panoid: 1199332008, pov: { pan: 287.35, tilt: 2.72, zoom: 0 } },
            { name: "세븐일레븐화성봉담수기점", addr: "경기 화성시 세자로", panoid: 1197741399, pov: { pan: 154.47, tilt: 0.15, zoom: 2 } },
            { name: "새상무복권", addr: "광주 서구 치평로", panoid: 1200264571, pov: { pan: 92.32, tilt: 0.07, zoom: -2 } },
            { name: "한아름매점", addr: "충남 홍성군 광천읍", panoid: 1160927365, pov: { pan: 23.96, tilt: -3.90, zoom: -3 } },
            { name: "차부상회", addr: "경기 김포시 통진읍", panoid: 1203538717, pov: { pan: 40.20, tilt: -1.06, zoom: -3 } },
            { name: "행복슈퍼", addr: "서울 성북구 동소문로", panoid: 1198249502, pov: { pan: 8.00, tilt: 11.80, zoom: -3 } },
            { name: "서해로또방", addr: "경기 화성시 화성로", panoid: 1196541229, pov: { pan: 347.47, tilt: 3.57, zoom: 1 } },
            { name: "용두천하", addr: "광주 북구 하서로", panoid: 1200286962, pov: { pan: 260.36, tilt: 6.67, zoom: 0 } },
            { name: "영훈슈퍼마켓", addr: "서울 도봉구 창3동", panoid: 1198487686, pov: { pan: 44.21, tilt: 2.30, zoom: -3 } },
            { name: "코리아마트(비산점)", addr: "대구 서구 국채보상로", panoid: 1201556335, pov: { pan: 2.80, tilt: 1.39, zoom: 0 } },
            { name: "원웨이로또 (폐점)", addr: "서울 서초구 서초동 1571-18 청화빌딩", isClosed: true, customMessage: "과거 6회 당첨 이력이 있으나 현재 폐점되었습니다." },
            { name: "원스탑", addr: "서울 송파구 백제고분로7길", panoid: 1197972914, pov: { pan: 27.06, tilt: -6.82, zoom: 0 } },
            // User Request: 3 Shops (260216-3)
            { name: "제일복권", addr: "경남 양산시 양산역2길", panoid: 1204952001, pov: { pan: 21.04, tilt: -3.52, zoom: 0 } },
            { name: "터미널식품", addr: "경기 의정부시 의정로", panoid: 1174621640, pov: { pan: 68.32, tilt: -2.09, zoom: 1 } },
            { name: "진양호", addr: "경남 진주시 남강로", panoid: 1192787482, pov: { pan: 245.24, tilt: 1.05, zoom: 3 } },
            // User Request: 13 Shops (260216-4)
            { name: "작은신부", addr: "충남 서산시 구진로", panoid: 1177372374, pov: { pan: 95.48, tilt: -0.98, zoom: 2 } },
            { name: "보경복권", addr: "울산 북구 명촌6길", panoid: 1202119790, pov: { pan: 349.51, tilt: 0.35, zoom: 1 } },
            { name: "로또야놀자", addr: "경북 경주시 양정로", panoid: 1187157120, pov: { pan: 265.02, tilt: 0.41, zoom: -2 } },
            { name: "로또또", addr: "경기 김포시 봉수대로", panoid: 1203018324, pov: { pan: 343.01, tilt: 1.95, zoom: -3 } },
            { name: "삼성포토랜드", addr: "인천 강화군 북문길", panoid: 1199442921, pov: { pan: 105.41, tilt: 2.36, zoom: -3 } },
            { name: "세븐일레븐 현풍대로점", addr: "대구 달성군 비슬로", panoid: 1200939879, pov: { pan: 198.04, tilt: -0.79, zoom: 0 } },
            { name: "우두로또", addr: "강원 춘천시 영서로", panoid: 1195653386, pov: { pan: 27.37, tilt: -1.48, zoom: 2 } },
            { name: "송내매표소", addr: "경기 부천시 소사구", panoid: 1203623206, pov: { pan: 303.66, tilt: -6.13, zoom: 2 } },
            { name: "온천로또방", addr: "대전 유성구 계룡로", panoid: 1200704937, pov: { pan: 260.53, tilt: -4.97, zoom: 2 } },
            { name: "한경종합광고", addr: "서울 송파구 백제고분로", panoid: 1197947148, pov: { pan: 210.81, tilt: 2.59, zoom: 3 } },
            { name: "그린로또", addr: "강원 양양군 양양로", panoid: 1196252686, pov: { pan: 175.22, tilt: -0.57, zoom: 1 } },
            { name: "호반할인마트", addr: "광주 광산구 도산로9번길", panoid: 1200129909, pov: { pan: 318.66, tilt: 1.75, zoom: -3 } },
            { name: "로또스튜디오", addr: "충북 청주시 청원구", panoid: 1170630295, pov: { pan: 53.76, tilt: 0.21, zoom: -3 } },
            // User Request: 6 Shops (260216-5)
            { name: "코사마트금강점", addr: "대구 달서구 용산로", panoid: 1201616618, pov: { pan: 87.20, tilt: 5.74, zoom: -3 } },
            { name: "황금대박점", addr: "서울 노원구 공릉로", panoid: 1197986422, pov: { pan: 75.30, tilt: 2.10, zoom: 2 } },
            { name: "봉황로또", addr: "전북 임실군 운수로", panoid: 1184544406, pov: { pan: 277.47, tilt: -7.51, zoom: 2 } },
            { name: "운수대통", addr: "인천 부평구 동암광장로", panoid: 1199147716, pov: { pan: 221.75, tilt: -1.58, zoom: 2 } },
            { name: "울릉로또", addr: "경북 울릉군 봉래2길", panoid: 1196322336, pov: { pan: 192.70, tilt: -3.11, zoom: -3 } },
            { name: "제주대림점", addr: "제주 제주시 과원북2길", panoid: 1182183945, pov: { pan: 156.35, tilt: -4.86, zoom: 1 } },
            // User Request: D-mart (260216-6)
            { name: "D-마트 담배", addr: "강원 속초시 조양상가길", panoid: 1196877412, pov: { pan: 235.90, tilt: -3.77, zoom: -3 }, customMessage: "롯데마트 내부 1층에 있습니다." },
            // User Request: 3 Shops (260216-7)
            { name: "스카이편의점", addr: "경기 안양시 만안구", panoid: 1202967509, pov: { pan: 172.54, tilt: -3.97, zoom: -3 } },
            { name: "이삭", addr: "전남 목포시 통일대로", panoid: 1192652943, pov: { pan: 346.05, tilt: -3.16, zoom: 1 } },
            { name: "대박유통", addr: "부산 중구 구덕로", panoid: 1202686590, pov: { pan: 326.06, tilt: -4.19, zoom: 1 } },
            // User Request: 6 Shops (260216-8)
            { name: "안성맞춤", addr: "경기 안성시 안성맞춤대로", panoid: 1176067110, pov: { pan: 201.02, tilt: 4.96, zoom: -2 } },
            { name: "신세계", addr: "제주 제주시 고마로14길", panoid: 1182352878, pov: { pan: 115.48, tilt: -1.66, zoom: -3 } },
            { name: "구담쌀슈퍼", addr: "경북 안동시 경동로", panoid: 1166243556, pov: { pan: 213.59, tilt: -1.80, zoom: -3 } },
            { name: "토토복권", addr: "대구 서구 달서로12길", panoid: 1201339587, pov: { pan: 9.12, tilt: -3.19, zoom: -3 } },
            { name: "우리은행금호동지점앞가판", addr: "서울 성동구 장터길", panoid: 1198891800, pov: { pan: 264.88, tilt: -10.57, zoom: -3 } },
            { name: "외동복권", addr: "경남 김해시 동남로49번길", panoid: 1193704600, pov: { pan: 167.72, tilt: -1.15, zoom: -3 } },
            // User Request: Closed Shop (260216-9)
            { name: "엘도라도복권전문점", addr: "서울 광진구 중곡동 124-65", isClosed: true, customMessage: "현재 폐점되었습니다." },
            // User Request: 3 Shops (260216-10)
            { name: "하프타임(괴정점)", addr: "부산 사하구 사하로", panoid: 1202279089, pov: { pan: 191.71, tilt: -0.16, zoom: -1 } },
            { name: "동홍코사마트", addr: "제주 서귀포시 동홍서로", panoid: 1181313516, pov: { pan: 92.42, tilt: 4.57, zoom: -3 } },
            { name: "토큰박스", addr: "경기 남양주시 진건오남로", panoid: 1185000546, pov: { pan: 209.59, tilt: 3.38, zoom: -3 } },
            // User Request: Today (260216-11)
            { name: "Today", addr: "서울 광진구 광나루로56길", panoid: 1198490195, pov: { pan: 148.43, tilt: -3.00, zoom: -3 }, customMessage: "테크노파크 9층에 매장있음" },
            // User Request: New Signboard (260216-12)
            { name: "신간판", addr: "서울 중구 무교동 12-1", panoid: 1198684037, pov: { pan: 77.59, tilt: -6.13, zoom: -1 }, customMessage: "곰국시집 앞 가판이 맞습니다." },
            // User Request: 2 Shops (260216-13)
            { name: "버스카드판매대", addr: "서울 관악구 신림로", panoid: 1198278084, pov: { pan: 223.84, tilt: -0.59, zoom: -3 } },
            { name: "마리오슈퍼", addr: "경기 부천시 송내대로265번길", panoid: 1203673840, pov: { pan: 188.39, tilt: -0.22, zoom: -1 }, customMessage: "뱅뱅프라자 1층 내부에 매장있음." },
            // User Request: 6 Shops (260216-14)
            { name: "원동슈퍼", addr: "충남 보령시 중앙로", panoid: 1176675568, pov: { pan: 101.32, tilt: 4.96, zoom: -3 } },
            { name: "현암꽃플라워", addr: "대전 동구 태전로", panoid: 1201410105, pov: { pan: 227.22, tilt: -2.16, zoom: -3 } },
            { name: "미래유통", addr: "전남 목포시 영산로", panoid: 1192393614, pov: { pan: 282.37, tilt: 1.75, zoom: -1 } },
            { name: "장군슈퍼", addr: "경기 부천시 오정구", panoid: 1203452762, pov: { pan: 315.13, tilt: -1.34, zoom: 0 } },
            { name: "신명", addr: "서울 강서구 방화2동", panoid: 1198209762, pov: { pan: 307.53, tilt: 0.56, zoom: 0 } },
            { name: "대광슈퍼", addr: "경기 군포시 고산로", panoid: 1175371099, pov: { pan: 334.69, tilt: -2.37, zoom: 2 } },
            // User Request: 9 Shops (260216-15)
            { name: "혹시나도", addr: "충북 음성군 감곡면", panoid: 1164851877, pov: { pan: 16.89, tilt: 5.51, zoom: 2 } },
            { name: "나라시스컴", addr: "서울 영등포구 영등포로", panoid: 1198373900, pov: { pan: 20.51, tilt: 2.58, zoom: 2 } },
            { name: "나눔이매로또", addr: "경기 성남시 분당구", panoid: 1199105925, pov: { pan: 313.10, tilt: 0.42, zoom: 1 } },
            { name: "대림통상", addr: "울산 중구 태화동", panoid: 1201823875, pov: { pan: 24.91, tilt: 3.83, zoom: 1 } },
            { name: "제일슈퍼", addr: "인천 연수구 앵고개로", panoid: 1199991356, pov: { pan: 303.39, tilt: 1.72, zoom: 0 } },
            { name: "경기상회", addr: "인천 남동구 만수동", panoid: 1199316390, pov: { pan: 177.01, tilt: 2.38, zoom: 1 } },
            { name: "스포츠베팅샵", addr: "서울 서초구 양재대로11길", panoid: 1198055141, pov: { pan: 182.79, tilt: 2.40, zoom: 2 } },
            { name: "우미슈퍼", addr: "광주 서구 풍암동", panoid: 1200542640, pov: { pan: 294.37, tilt: 1.70, zoom: 2 } },
            { name: "진성식품", addr: "충북 제천시 의병대로", panoid: 1185296414, pov: { pan: 197.87, tilt: -0.77, zoom: 1 } },
            // User Request: 18 Recovered Shops (260216-2)
            { name: "사이버정보통신", addr: "부산 부산진구 동평로", panoid: 1202364869, pov: { pan: 37.89, tilt: 2.99, zoom: -2 } },
            { name: "나눔로또편의점", addr: "전남 광양시 공영로", panoid: 1205201589, pov: { pan: 183.29, tilt: -2.32, zoom: -1 } },
            { name: "율암25시편의점", addr: "경기 화성시 시청로", panoid: 1198087972, pov: { pan: 158.58, tilt: 1.36, zoom: 0 } },
            { name: "해피+24시편의점", addr: "광주 북구 하서로", panoid: 1200291324, pov: { pan: 84.83, tilt: 1.48, zoom: -3 } },
            { name: "흥양마중물", addr: "강원 원주시 치악로", panoid: 1195199655, pov: { pan: 305.15, tilt: 13.98, zoom: -2 } },
            { name: "복권마트 & 씨스페이스 홍천점", addr: "강원 홍천군 홍천로", panoid: 1197150362, pov: { pan: 307.89, tilt: 2.54, zoom: -2 } },
            { name: "한국인세계대박복권", addr: "인천 연수구 독배로197번길", panoid: 1200648162, pov: { pan: 281.03, tilt: -2.90, zoom: -2 } },
            { name: "하이로또", addr: "서울 금천구 금하로", panoid: 1198115190, pov: { pan: 209.13, tilt: -1.64, zoom: -2 } },
            { name: "충남상회", addr: "인천 미추홀구 참외전로", panoid: 1199332008, pov: { pan: 287.35, tilt: 2.72, zoom: 0 } },
            { name: "세븐일레븐화성봉담수기점", addr: "경기 화성시 세자로", panoid: 1197741399, pov: { pan: 154.47, tilt: 0.15, zoom: 2 } },
            { name: "새상무복권", addr: "광주 서구 치평로", panoid: 1200264571, pov: { pan: 92.32, tilt: 0.07, zoom: -2 } },
            { name: "한아름매점", addr: "충남 홍성군 광천읍", panoid: 1160927365, pov: { pan: 23.96, tilt: -3.90, zoom: -3 } },
            { name: "차부상회", addr: "경기 김포시 통진읍", panoid: 1203538717, pov: { pan: 40.20, tilt: -1.06, zoom: -3 } },
            { name: "행복슈퍼", addr: "서울 성북구 동소문로", panoid: 1198249502, pov: { pan: 8.00, tilt: 11.80, zoom: -3 } },
            { name: "서해로또방", addr: "경기 화성시 화성로", panoid: 1196541229, pov: { pan: 347.47, tilt: 3.57, zoom: 1 } },
            { name: "용두천하", addr: "광주 북구 하서로", panoid: 1200286962, pov: { pan: 260.36, tilt: 6.67, zoom: 0 } },
            { name: "영훈슈퍼마켓", addr: "서울 도봉구 창3동", panoid: 1198487686, pov: { pan: 44.21, tilt: 2.30, zoom: -3 } },
            { name: "코리아마트(비산점)", addr: "대구 서구 국채보상로", panoid: 1201556335, pov: { pan: 2.80, tilt: 1.39, zoom: 0 } },
            { name: "교통카드판매대", addr: "서울 강동구 고덕동 210-1", isClosed: true, customMessage: "현재 폐점되었습니다 (구서울승합종점앞 가판대)." },
            { name: "부일카서비스", addr: "부산 동구 범일동", panoId: 1202519412, pov: { pan: 236.39, tilt: 6.54, zoom: -3 } },
            { name: "일등복권편의점", addr: "대구 달서구 본리동", panoId: 1201526676, pov: { pan: 349.47, tilt: 12.34, zoom: -1 } },
            // User Request: Buheung Fruit (260216-16) - Verified from Link
            { name: "부흥청과식품점", addr: "경북 경산시 하양읍 금락리", panoid: 1187452657, pov: { pan: 293.20, tilt: -0.90, zoom: 0 } },
            // User Request: Buyeong Mart (260216-17) - Verified Final Location (Jungnang-yeok-ro 9)
            { name: "부영마트", addr: "서울 중랑구 상봉동", panoid: 1198489183, pov: { pan: 85.38, tilt: 2.03, zoom: 1 }, customMessage: "최종 이전: 중랑역로 9 (상봉동 108/면목로 481 통합)" },
            // User Request: Lucky Super (260216-18) - Verified Relocation
            { name: "럭키슈퍼", addr: "서울 용산구 후암동", panoid: 1197374162, pov: { pan: 79.24, tilt: 0.96, zoom: 2 }, customMessage: "후암동 446 -> 후암로 52 (이전/동일매장)" },
            // User Request: Jun (260216-18)
            { name: "준", addr: "경기 평택시 포승읍", panoid: 1196771227, pov: { pan: 103.33, tilt: -2.22, zoom: 2 } },
            { name: "스파", addr: "서울 노원구 상계동", panoId: 1198397843, pov: { pan: 316.53, tilt: 2.76, zoom: -1 } },
            { name: "로또명당인주점", addr: "충남 아산시 서해로", panoId: 1152034899, pov: { pan: 324.00, tilt: 3.71, zoom: -3 } },
            { name: "뉴빅마트", addr: "부산 기장군 정관중앙로", panoId: 1202061273, pov: { pan: 113.90, tilt: -1.64, zoom: 1 } },
            { name: "부일카서비스", addr: "부산 동구 자성로133번길", panoId: 1202519408, pov: { pan: 230.15, tilt: 0.33, zoom: -1 } },
            { name: "로또휴게실", addr: "경기 용인시 기흥구", panoId: 1199447932, pov: { pan: 260.1, tilt: -1.2, zoom: 3 } },
            { name: "오천억복권방", addr: "광주 서구 상무대로", panoId: 1200299139, pov: { pan: 342.32, tilt: 2.52, zoom: 1 } },
            { name: "로또명당인주점", addr: "충남 아산시 인주면", panoId: 1176307856, pov: { pan: 281.23, tilt: 3.29, zoom: 2 } },
            { name: "스파", addr: "서울 노원구 동일로 1493", panoId: 1198397843, pov: { pan: 318.09, tilt: -0.61, zoom: 0 } },
            { name: "왕대박복권방", addr: "경북 문경시 중앙로", panoId: 1184892306, pov: { pan: 308.56, tilt: 3.85, zoom: 2 } },
            { name: "알리바이", addr: "광주 광산구 수등로", panoId: 1199874247, pov: { pan: 70.76, tilt: -0.16, zoom: -3 } },
            { name: "오케이상사", addr: "서울 서초구 신반포로 176 (반포동)", panoId: 1018301543, pov: { pan: 184.52, tilt: 10.0, zoom: 0 } },
            { name: "잠실매점", addr: "서울 송파구 올림픽로 269 1층 (잠실역 8번출구 앞)", panoId: 1197820708, pov: { pan: 355.0, tilt: -0.3, zoom: 1 } },
            { name: "월드컵복권방", addr: "경기 광주시 경안로 20", panoId: 1202723374, pov: { pan: 11.5, tilt: -0.6, zoom: 0 } },
            { name: "갈렙분식한식", addr: "서울 중랑구 망우동", panoId: 1198253759, pov: { pan: 108.88, tilt: 0.41, zoom: -3 } },
            { name: "로또킹", addr: "서울 영등포구 영중로", panoId: 1171055517, pov: { pan: 21.23, tilt: -4.98, zoom: 0 } },
            { name: "돈벼락맞는곳", addr: "부산 동구 조방로49번길", panoId: 1202542575, pov: { pan: 1.35, tilt: -5.08, zoom: 0 } },
            { name: "중앙로또", addr: "경북 칠곡군 북삼로", panoId: 1167169878, pov: { pan: 323.40, tilt: 1.02, zoom: -3 } },
            { name: "또또복권방", addr: "전북 익산시 영등동", panoId: 1179975829, pov: { pan: 357.24, tilt: 0.52, zoom: 1 } },
            { name: "썬마트", addr: "충북 청주시 흥덕구", panoId: 1170640105, pov: { pan: 272.68, tilt: 4.98, zoom: 1 } },
            { name: "복권명당(서부점)", addr: "대구 달서구 송현동", panoId: 1201394989, pov: { pan: 133.15, tilt: 0.06, zoom: 1 } },
            { name: "월드24시", addr: "서울 은평구 갈현1동", panoId: 1197925499, pov: { pan: 174.22, tilt: -0.80, zoom: 0 } },
            { name: "썬마트", addr: "충북 청주시 흥덕구", panoId: 1170639962, pov: { pan: 332.05, tilt: 1.41, zoom: -3 } },
            { name: "라이프마트", addr: "인천 중구 항동7가", panoId: 1198808458, pov: { pan: 283.89, tilt: 8.44, zoom: 0 } },
            { name: "영광정보통신", addr: "서울 성북구 하월곡동 37-18", panoId: 1198189825, pov: { pan: 119.8, tilt: -5.0, zoom: 0 } },
            { name: "가판점(신문)", addr: "서울 영등포구 당산동6가 331-1", panoId: 1198369749, pov: { pan: 25.60, tilt: 3.30, zoom: 0 } },
            { name: "묵동식품", addr: "서울 중랑구 묵동 238-11", panoId: 1198447963, pov: { pan: 268.85, tilt: 2.27, zoom: 3 } },
            { name: "목화휴게소", addr: "경남 사천시 용현면", panoId: 1188432049, pov: { pan: 103.75, tilt: 8.02, zoom: 1 } },
            { name: "목화휴게소", addr: "경남 사천시 사천대로 912", panoId: 1188272977, pov: { pan: 34.24, tilt: 0.74, zoom: 0 } },
            { name: "복권백화점", addr: "경기 파주시 평화로", panoid: 1202862935, pov: { pan: 48.22, tilt: 2.81, zoom: 1 } },
            { name: "복권백화점(대백.한라앞)", addr: "대구 달서구 이곡동", panoid: 1201505680, pov: { pan: 341.21, tilt: 4.46, zoom: 0 } },
            { name: "영화유통(1등복권방)", addr: "울산 남구 신정로", panoId: 1202168610, pov: { pan: 262.28, tilt: 6.84, zoom: -3 } },
            { name: "종합복권슈퍼", addr: "경기 시흥시 마유로", panoId: 1175858045, pov: { pan: 129.49, tilt: 4.68, zoom: 3 } },
            { name: "한꿈복권방", addr: "울산 중구 번영로", panoId: 1202017794, pov: { pan: 168.99, tilt: -1.41, zoom: 3 } },
            { name: "현대장미슈퍼", addr: "전북 익산시 동서로61길", panoId: 1179925999, pov: { pan: 216.02, tilt: 2.46, zoom: -1 } },
            { name: "북마산복권전문점", addr: "경남 창원시 마산합포구", panoId: 1204481175, pov: { pan: 94.99, tilt: 4.55, zoom: -3 } },
            { name: "행운복권방", addr: "경기 포천시 소흘읍 죽엽산로 438", panoId: 1175632287, pov: { pan: 113.99, tilt: -9.48, zoom: 0 } },
            { name: "행운복권방 보생당건강원", addr: "전북 익산시 무왕로 1268", panoId: 1179789585, pov: { pan: 168.69, tilt: -0.46, zoom: -2 } },
            { name: "행운복권방", addr: "경기 의정부시 용현동", panoId: 1174558837, pov: { pan: 255.27, tilt: -1.13, zoom: -3 } },
            { name: "일등복권편의점", addr: "대구 달서구 대명천로 220", panoId: 1201526676, pov: { pan: 350.40, tilt: 1.57, zoom: -1 } },
            { name: "하늘로또", addr: "경기 여주시 세종로475번길", panoId: 1175070156, pov: { pan: 49.17, tilt: 3.23, zoom: 2 } },
            { name: "빅세일복권방", addr: "부산 부산진구 서면문화로", panoId: 1202698289, pov: { pan: 104.61, tilt: -2.96, zoom: 3 } },
            { name: "로또열풍 (세진전자통신)", addr: "대구 서구 서대구로 156", panoId: 1201585664, pov: { pan: 83.32, tilt: 2.46, zoom: -3 } },
            { name: "복권나라", addr: "서울 관악구 남부순환로 1739-9", panoId: 1198285612, pov: { pan: 330.0, tilt: 10.0, zoom: 2 } },
            { name: "다니엘사", addr: "경기 안산시 단원구 원선1로 38 101호", panoId: 1204134596, pov: { pan: 356.2, tilt: -3.0, zoom: 4 } },
            { name: "이마트24 순천산단점", addr: "전남 순천시 산단1길 6", panoId: 1173643437, pov: { pan: 257.9, tilt: 3.2, zoom: 3 } },
            { name: "제이복권방", addr: "서울 종로구 종로", panoId: 1197815068, pov: { pan: 356.05, tilt: -1.00, zoom: -1 } },
            { name: "복권명당", addr: "대전 서구 만년동 112", panoId: 1200850347, pov: { pan: 250.0, tilt: 10.3, zoom: 0 } },
            { name: "대박마트복권방", addr: "충남 아산시 음봉면", panoId: 1176849717, pov: { pan: 219.56, tilt: 2.64, zoom: 0 } },
            { name: "평안당", addr: "서울 종로구 종로5가", panoId: 1197815101, pov: { pan: 337.91, tilt: 6.03, zoom: 0 } },
            { name: "대박복권방", addr: "경기 연천군 전곡읍", panoId: 1175550133, pov: { pan: 258.57, tilt: -1.93, zoom: -3 } },
            { name: "알리바이(나주점)", addr: "전남 나주시 금성동", panoId: 1191260191, pov: { pan: 104.99, tilt: -1.23, zoom: -3 } },
            { name: "토큰판매소", addr: "서울 송파구 풍납1동", panoId: 1198482657, pov: { pan: 281.96, tilt: 5.56, zoom: 1 } },
            { name: "행복충전소", addr: "경기 평택시 지산동", panoId: 1198299520, pov: { pan: 118.12, tilt: 4.47, zoom: -2 } },
            { name: "NG24", addr: "경북 칠곡군 석적읍", panoId: 1166639892, pov: { pan: 332.83, tilt: 10.69, zoom: -2 } },
            { name: "소리창고", addr: "서울 강서구 내발산동", panoId: 1198604052, pov: { pan: 104.79, tilt: 1.68, zoom: -1 } },
            { name: "팡팡복권마트.잡화슈퍼", addr: "전북 전주시 덕진구", panoId: 1171843139, pov: { pan: 340.71, tilt: 2.47, zoom: -1 } },
            { name: "황금로또", addr: "강원 원주시 태장2동 1390-16", panoid: 1196038632, pov: { pan: 222.54, tilt: 1.87, zoom: -3 } },
            { name: "로또복권두정점", addr: "충남 천안시 서북구", panoId: 1195549516, pov: { pan: 4.85, tilt: 6.66, zoom: -3 } },
            { name: "대산슈퍼", addr: "충남 천안시 동남구", panoId: 1193995561, pov: { pan: 182.45, tilt: 4.26, zoom: -2 } },
            { name: "에스비 상사", addr: "서울 중구 퇴계로86길 29", panoid: 1198788741, pov: { pan: 68.90, tilt: 4.57, zoom: -3 } },
            { name: "청솔서점", addr: "부산 사하구 하신번영로", panoId: 1161907485, pov: { pan: 192.32, tilt: 5.42, zoom: -1 } },
            { name: "대전우표사", addr: "대전 동구 중앙로204번길", panoId: 1163576030, pov: { pan: 55.45, tilt: 1.93, zoom: -3 } },
            { name: "주택복권방", addr: "경기 용인시 수지구", panoId: 1199750326, pov: { pan: 141.11, tilt: 3.85, zoom: 1 } },
            { name: "미나식품(로또판매점)", addr: "서울 강서구 금낭화로", panoId: 1198192808, pov: { pan: 323.87, tilt: -2.11, zoom: -3 } },
            { name: "나눔로또봉평점", addr: "경남 통영시 도남로 81", panoId: 1204285725, pov: { pan: 15.6, tilt: 2.0, zoom: -1 } },
            { name: "천하명당", addr: "경기 시흥시 신천3길", panoId: 1175741916, pov: { pan: 335.65, tilt: 6.06, zoom: -2 } },
            { name: "로터리복권방", addr: "부산 서구 자갈치로 4-1 1층", panoid: 1202119889, pov: { pan: 175.81, tilt: 2.55, zoom: -1 } },
            { name: "천하명당복권방", addr: "경남 거제시 옥포성안로", panoId: 1204368030, pov: { pan: 96.19, tilt: 6.22, zoom: -1 } },
            { name: "신문가판점", addr: "서울 용산구 한강대로", panoId: 1197632086, pov: { pan: 256.46, tilt: 4.87, zoom: -3 } },
            { name: "대운", addr: "경기 김포시 대명항로", panoId: 1203824304, pov: { pan: 177.65, tilt: 9.98, zoom: 0 } },
            { name: "세계로생활가전", addr: "서울 동작구 보라매로", panoId: 1197780011, pov: { pan: 92.74, tilt: 5.30, zoom: -2 } },
            { name: "노다지복권방", addr: "인천 미추홀구 한나루로", panoId: 1199931642, pov: { pan: 128.28, tilt: 0.08, zoom: -3 } },
            { name: "노다지복권방", addr: "경기 용인시 처인구 금령로 130", panoId: 1198887321, pov: { pan: 154.07, tilt: 7.36, zoom: 1 }, customMessage: "이 매장은 2020년경 마평동 735-1에서 현 위치로 이전했습니다. 총 1등 당첨 11회 (구점포 6회 + 현점포 5회)" },
            { name: "알리바이(나주점)", addr: "전남 나주시 나주로 142 알리바이", panoId: 1191260182, pov: { pan: 17.27, tilt: -9.34, zoom: -3 } },
            { name: "노다지복권방", addr: "경기 시흥시 대야동 345-16 1층상가", panoId: 1175484799, pov: { pan: 246.25, tilt: 2.60, zoom: -2 } },
            { name: "오천억복권방", addr: "광주 서구 화정동 782-14", panoId: 1200299139, pov: { pan: 357.21, tilt: 0.33, zoom: -3 } },
            { name: "미나식품(로또판매점)", addr: "서울 강서구 방화동 484-23", panoId: 1198192808, pov: { pan: 342.76, tilt: 0.59, zoom: -3 } },
            { name: "복권전문점", addr: "인천 부평구 청천동 236-20", panoId: 1199144048, pov: { pan: 341.21, tilt: 2.94, zoom: -3 } },
            { name: "복권명당", addr: "충남 공주시 신관동 585-12", panoId: 1179373419, pov: { pan: 305.44, tilt: 0.77, zoom: -3 } },
            { name: "영화유통(1등복권방)", addr: "울산 남구 달동 758삼성아파트상가204-101", panoId: 1202168610, pov: { pan: 245.1, tilt: 2.0, zoom: 0 } },
            { name: "복권나라", addr: "서울 관악구 남부순환로 1739-9", panoId: 1198432279, pov: { pan: 157.71, tilt: 11.97, zoom: -3 } },
            { name: "대박천하마트", addr: "인천 부평구 굴포로", panoId: 1198907645, pov: { pan: 105.07, tilt: 4.60, zoom: -2 } },
            { name: "대박천하마트", addr: "인천 부평구 갈산동 367번지", panoId: 1199224040, pov: { pan: 190.56, tilt: -6.41, zoom: -3 } },
            { name: "대박슈퍼", addr: "인천 부평구 경원대로", panoId: 1199058573, pov: { pan: 177.81, tilt: -2.27, zoom: 1 } },
            { name: "진평양행", addr: "강원 강릉시 임영로", panoId: 1194087150, pov: { pan: 256.26, tilt: -4.05, zoom: -1 } },
            { name: "운좋은날", addr: "서울 강동구 풍성로", panoId: 1198599079, pov: { pan: 11.15, tilt: 3.08, zoom: -1 } },
            { name: "바이더웨이녹번중앙점", addr: "서울 은평구 녹번동", panoid: 1197941920, pov: { pan: 7.17, tilt: 4.71, zoom: 2 } },
            { name: "포항오거리CU복권", addr: "경북 포항시 북구 죽도로 33", panoid: 1187942783, pov: { pan: 98.45, tilt: -3.21, zoom: -3 } },
            { name: "꾸미로또복권", addr: "서울 강북구 솔샘로67길 118", panoid: 1197850243, pov: { pan: 140.19, tilt: 4.97, zoom: -3 } },
            { name: "복권전문점", addr: "경기 시흥시 중심상가로", panoId: 1176040872, pov: { pan: 38.81, tilt: 7.94, zoom: 0 } },
            { name: "세븐복권방", addr: "경기 파주시 해올2길 16", panoid: 1203125581, pov: { pan: 349.39, tilt: -3.14, zoom: 2 } },
            { name: "짱복권", addr: "서울 종로구 종로 269", panoid: 1197814790, pov: { pan: 0.65, tilt: -0.16, zoom: 2 } },
            { name: "행운복권방", addr: "경기 의정부시 충의로 55", panoId: 1174093159, pov: { pan: 277.0, tilt: 0.0, zoom: 0 } },
            { name: "왕대박복권 (인더라인)", addr: "인천 부평구 십정동 577-6", panoId: 1203625174, pov: { pan: 190.23, tilt: -5.06, zoom: -3 } },
            { name: "프렌드24시", addr: "광주 광산구 첨단중앙로 164", panoid: 1199708554, pov: { pan: 171.41, tilt: -6.19, zoom: 1 } },
            { name: "알리바이금당점", addr: "전남 순천시 대석길", panoId: 1173674879, pov: { pan: 359.32, tilt: 3.55, zoom: -2 } },
            { name: "해뜰날", addr: "경기 동두천시 중앙로", panoId: 1175647022, pov: { pan: 167.43, tilt: 0.87, zoom: 0 } },
            { name: "노다지복권방", addr: "경기 용인시 처인구 마평동 735-1", panoId: 1198953144, pov: { pan: 126.6, tilt: 2.2, zoom: 2 } },
            { name: "GS25(계산동경점)", addr: "인천 계양구 계산동", panoid: 1199151424, pov: { pan: 353.80, tilt: -2.31, zoom: -2 } },
            { name: "창원병원앞매표소", addr: "경남 창원시 성산구", panoid: 1204481691, pov: { pan: 36.51, tilt: 4.43, zoom: 2 } },
            { name: "역전광장상회", addr: "경기 파주시 금촌1동 329-19", panoid: 1203271929, pov: { pan: 158.43, tilt: 1.88, zoom: 1 } },
            { name: "복권방", addr: "부산 부산진구 당감동", panoid: 1202678221, pov: { pan: 228.64, tilt: 1.60, zoom: -2 } },
            { name: "대광복권방", addr: "전남 화순군 화순읍 대리 97-3", panoId: 1192902741, pov: { pan: 339.4, tilt: 4.4, zoom: 0 } },
            { name: "명당골복권방", addr: "경기 수원시 권선구", panoId: 1199751659, pov: { pan: 187.22, tilt: 5.79, zoom: -3 } },
            { name: "다터져복권방", addr: "경기 평택시 합정동", panoid: 1197642715, pov: { pan: 284.10, tilt: 1.67, zoom: -3 } },
            { name: "행운의집", addr: "경북 안동시 북문동 23-7", isClosed: true, customMessage: "현재는 폐업상태의 점포입니다" },
            { name: "지원물산", addr: "서울 노원구 공릉동", panoId: 1198350307, pov: { pan: 61.24, tilt: -1.90, zoom: -3 } },
            { name: "데이션나잇", addr: "서울 성북구 종암동 132", panoId: 1198236406, pov: { pan: 52.6, tilt: 10.3, zoom: 0 } },
            { name: "파란만장복권방", addr: "경기 화성시 진안동", panoId: 1198278713, pov: { pan: 156.78, tilt: -2.10, zoom: 3 } },
            { name: "황실복권방", addr: "충남 천안시 동남구", panoId: 1193993670, pov: { pan: 346.95, tilt: 4.35, zoom: 3 } },
            { name: "GS25(대전시네마점)", addr: "대전 서구 괴정동", panoId: 1201429942, pov: { pan: 132.97, tilt: 5.70, zoom: -3 } },
            { name: "로또복권역전점", addr: "경북 경주시 노서동", panoid: 1187221443, pov: { pan: 58.22, tilt: -0.16, zoom: 0 } },
            { name: "셀프카메라", addr: "부산 부산진구 개금동", panoId: 1202587961, pov: { pan: 100.14, tilt: -0.54, zoom: -3 } },
            { name: "올인(allin)", addr: "경기 화성시 향남읍", panoId: 1197247800, pov: { pan: 301.07, tilt: 9.93, zoom: -3 } },
            { name: "로또복권방", addr: "경기 용인시 처인구", panoId: 1199530907, pov: { pan: 306.53, tilt: 1.09, zoom: 0 } },
            { name: "버스판매소", addr: "서울 영등포구 영등포동4가 441-10", panoId: 1198368804, pov: { pan: 64.0, tilt: 0.9, zoom: 0 } },
            { name: "GS25(양산문성)", addr: "경남 양산시 평산동 31-5", panoId: 1204592950, pov: { pan: 269.6, tilt: 1.0, zoom: 1 } },
            { name: "우리들공업탑점", addr: "울산 남구 신정동", panoid: 1201811174, pov: { pan: 25.20, tilt: 4.52, zoom: 2 } },
            { name: "메트로센터점", addr: "대구 중구 덕산동 88 (달구벌대로 지하 2100) C412호", imageUrl: "assets/img/metro_260213.jpg", customMessage: "반월당역 지하상가(C412호) 중심부에 위치하고 있습니다. (기존 4회 + 로드명주소 5회 합산 총 9회 당첨)" },
            { name: "행복한사람들(흥부네)", addr: "경기 광주시 경충대로 763 (초월읍 산이리 13-1)", imageUrl: "assets/img/happypeople_260213.jpg", customMessage: "이 점포는 도로 인접성 문제로 로드뷰 제공이 어려워 현장 사진으로 대체합니다. (기존 1회 + 도로명주소 5회 합산 총 6회 당첨)" },
            { name: "인터넷 복권판매사이트", addr: "서울특별시 서초구 남부순환로", customLink: "https://www.dhlottery.co.kr/userGuide", customMessage: "동 판매점은 온라인 구매가능한 동행복권 싸이트로 연결드립니다." },
            { name: "25시슈퍼", addr: "함송로14번길 13-17", panoId: 1176030807, pov: { pan: 310.46, tilt: 0.85, zoom: -1 } },
            { name: "복권판매점", addr: "동탄중심상가2길 37 1층으", panoId: 1198012866, pov: { pan: 212.35, tilt: -1.20, zoom: -2 } },
            { name: "(I.A) 로또마트", addr: "경기 안산시 단원구", panoid: 1204115898, pov: { pan: 181.61, tilt: 0.91, zoom: -3 } },
            { name: "1등로또방", addr: "광주 동구 중앙로", panoid: 1200326817, pov: { pan: 308.61, tilt: 15.32, zoom: 0 } },
            { name: "1등명당", addr: "충남 서천군 장항로", panoid: 1177595058, pov: { pan: 210.48, tilt: 5.06, zoom: -3 } },
            { name: "1번지복권방", addr: "경기 성남시 중원구", panoid: 1198797521, pov: { pan: 186.72, tilt: 0.43, zoom: -3 } },
            { name: "CU(거제해금강)", addr: "경남 거제시 고현동", panoid: 1204667361, pov: { pan: 283.99, tilt: 2.14, zoom: 1 } },
            { name: "CU(달동초이스점)", addr: "울산 남구 달동", panoid: 1202053722, pov: { pan: 125.30, tilt: 5.99, zoom: 1 } },
            { name: "CU(제천역점)", addr: "충북 제천시 화산동", panoid: 1185322618, pov: { pan: 176.31, tilt: 1.59, zoom: 1 } },
            { name: "CU노서점", addr: "경북 경주시 금성로259번길", panoid: 1187221443, pov: { pan: 51.09, tilt: 3.66, zoom: -1 } },
            { name: "GMART", addr: "경북 구미시 구미중앙로", panoid: 1165801425, pov: { pan: 10.82, tilt: 3.71, zoom: 0 } },
            { name: "GS25(고양주교점)", addr: "경기 고양시 덕양구", panoid: 1203877767, pov: { pan: 206.52, tilt: -2.65, zoom: -1 } },
            { name: "GS25(구로제일)", addr: "서울 구로구 구로동", panoid: 1198518853, pov: { pan: 259.12, tilt: -0.82, zoom: 0 } },
            { name: "GS25(청주수곡점)", addr: "충북 청주시 서원구", panoid: 1170580086, pov: { pan: 231.04, tilt: 2.27, zoom: 0 } },
            { name: "Goodday복권전문점", addr: "경남 창원시 성산구", panoid: 1204230685, pov: { pan: 322.84, tilt: 9.00, zoom: -3 } },
            { name: "LG슈퍼", addr: "경기 광명시 철산동", panoid: 1203337015, pov: { pan: 49.06, tilt: 1.76, zoom: -3 } },
            { name: "SK@24시편의점", addr: "경기 파주시 아동동 589-10", isClosed: true, customMessage: "현재 폐점된 매장입니다." },
            { name: "GS25(안산산호)", addr: "경기 안산시 단원구 선부동 1081산호한양상가101호", imageUrl: "assets/img/GS 안산산호점_260214.jpg", customMessage: "산호한양상가 1층에 위치한 GS25 편의점입니다." },
            { name: "가판", addr: "서울 마포구 도화2동 169 고려2 앞가판", isClosed: true, customMessage: "현재 폐점되었습니다 (가든호텔정문옆가판으로 이전 확인)" },
            { name: "가판 창동역점", addr: "서울 도봉구 창동 3-3 창동역문화마당앞", isClosed: true, customMessage: "현재 해당 위치의 가로판매대는 폐점되었거나 이전되었습니다." },
            { name: "가판점", addr: "서울 서초구 서초동(서초3동) 1602-2 가판", isClosed: true, customMessage: "현재 폐점된 가판대입니다." },
            { name: "가로가판대", addr: "서울 관악구 신림동(조원동) 1643-6" },
            { name: "가로판매대", addr: "서울 강동구 올림픽로 648 천호역 3번 출구 앞(가판점)" },
            { name: "가로판매점", addr: "서울 용산구 원효로 179", panoid: 1197440869, pov: { pan: 297.07, tilt: -5.58, zoom: -2 }, customMessage: "신한은행(ATM) 옆 가판점입니다. (주차부스 바로 옆 확인)" },
            { name: "고덕로또복권", addr: "서울 강동구 상일로15길 18 1층 (상일동역 4번 출구)", panoid: 1198588621, pov: { pan: 4.14, tilt: 4.14, zoom: 1 }, customMessage: "고덕로 397에서 이전한 6회 당첨 명당입니다." },
            { name: "가로판매대", addr: "서울 종로구 교남동", panoid: 1201585664, pov: { pan: 87.39, tilt: 13.86, zoom: -2 } },
            { name: "가자복권천국", addr: "전남 목포시 상동", panoid: 1192597069, pov: { pan: 352.61, tilt: -0.23, zoom: 3 } },
            { name: "가든호텔정문옆가판", addr: "서울 마포구 도화동 169-1", panoid: 1197820704, pov: { pan: 109.3, tilt: -0.9, zoom: 0 } },
            { name: "건강마트", addr: "경기 하남시 신장2동", panoid: 1173493468, pov: { pan: 130.32, tilt: 5.56, zoom: -2 } },
            { name: "경동G-PLUS할인마트", addr: "부산 해운대구 좌동", panoid: 1202480351, pov: { pan: 217.60, tilt: 6.09, zoom: 3 } },
            { name: "경성식품", addr: "서울 동대문구 휘경1동", panoid: 1198205251, pov: { pan: 15.21, tilt: 3.58, zoom: 0 } },
            { name: "공원슈퍼", addr: "경기 수원시 장안구", panoid: 1199575474, pov: { pan: 327.50, tilt: 4.59, zoom: -2 } },
            { name: "교하로또판매점", addr: "경기 파주시 파주로", panoid: 1203181718, pov: { pan: 275.18, tilt: -2.11, zoom: -3 } },
            { name: "구산복권방", addr: "경남 김해시 구산동", panoid: 1193912431, pov: { pan: 241.41, tilt: 0.35, zoom: 0 } },
            { name: "구포라인점", addr: "부산 북구 구포동", panoid: 1202526440, pov: { pan: 256.93, tilt: -2.56, zoom: 0 } },
            { name: "굿타임", addr: "서울 서대문구 연희동 353-94", panoid: 1197871361, pov: { pan: 194.7, tilt: 0.3, zoom: 0 } },
            { name: "그린마트", addr: "경기 성남시 분당구 대왕판교로 255 107호", panoid: 1198963691, pov: { pan: 274.7, tilt: 1.2, zoom: 4 } },
            { name: "그린마트", addr: "서울 송파구 백제고분로19길", panoid: 1197973342, pov: { pan: 85.96, tilt: 9.15, zoom: -2 } },
            { name: "금강복권", addr: "경기 김포시 율생로 3", panoid: 1203805177, pov: { pan: 152.85, tilt: 5.78, zoom: 0 } },
            { name: "기장슈퍼", addr: "부산 기장군 차성동로 69", panoid: 1033564888, pov: { pan: 350.25, tilt: 1.40, zoom: -3 } },
            { name: "까치복권방", addr: "경기 시흥시 중심상가로 326 1동 102호", panoid: 1176040887, pov: { pan: 245.5, tilt: -0.8, zoom: 1 } },
            { name: "나나 복권판매소", addr: "경남 양산시 상북면 상북중앙로 319", panoid: 1204563526, pov: { pan: 275.4, tilt: 0.6, zoom: 3 }, customMessage: "석계리 272-18에서 이전된 1등 5회 명당입니다. (상북중앙로 319 위치)" },
            { name: "나래복권", addr: "충북 충주시 충원대로 952", panoid: 1163813266, pov: { pan: 104.78, tilt: 1.24, zoom: 2 }, isClosed: true, customMessage: "현재 폐점 또는 로또 판매 중단 상태입니다. (과거 1등 4회 명당)" },
            { name: "넝쿨째(블루25 중앙점)", addr: "경남 창원시 마산합포구 중앙동2가 2-280", panoid: 1204644268, pov: { pan: 309.7, tilt: -9.2, zoom: 1 }, customMessage: "788회차에서 1등 3명이 동시에 배출된 진기록의 명당입니다." },
            { name: "노다지로또", addr: "인천 서구 완정로 179 검단제이원빌딩 108호", panoid: 1199025335, pov: { pan: 205.74, tilt: -0.60, zoom: -3 } },
            { name: "노다지복권방", addr: "부산 북구 덕천로 287", panoid: 1202267577, pov: { pan: 19.9, tilt: 6.4, zoom: 2 } },
            { name: "노다지복권방", addr: "인천 미추홀구 학익동 264-6 외7필지 125호", panoid: 1172510557, pov: { pan: 107.12, tilt: 11.54, zoom: -3 } },
            { name: "노다지복권방", addr: "서울 종로구 창신동 302-5", panoid: 1197814475, pov: { pan: 347.36, tilt: 4.46, zoom: -2 } },
            { name: "노다지복권방", addr: "경기 오산시 오산동 394-1", panoid: 1174611564, pov: { pan: 162.70, tilt: 10.85, zoom: -3 } },
            { name: "노다지복권방서정지점", addr: "경기 평택시 서정동 335-27", panoid: 1198305791, pov: { pan: 277.1, tilt: 2.9, zoom: 1 } },
            { name: "다드림복권", addr: "경기 김포시 월하로 930 1층 101호", panoid: 1203372471, pov: { pan: 231.20, tilt: 8.58, zoom: -3 } },
            { name: "당하복권명당", addr: "인천 서구 서곶로 788", panoid: 1199615169, pov: { pan: 68.28, tilt: 1.45, zoom: -3 } },
            { name: "대박", addr: "경기 구리시 안골로103번길 46", panoid: 1203302213, pov: { pan: 356.83, tilt: 0.69, zoom: -1 } },
            { name: "대박로또판매점", addr: "경기 수원시 장안구 영화로 2129-1 인동", panoid: 1199673044, pov: { pan: 243.99, tilt: 0.39, zoom: -3 } },
            { name: "대박마트", addr: "충남 천안시 동남구 봉명동 494 봉명청솔아파트상가 103호", panoid: 1194827511, pov: { pan: 284.9, tilt: -5.5, zoom: 0 } },
            { name: "대박명당", addr: "경기 양주시 옥정동로5길 6", panoid: 1204022501, pov: { pan: 342.4, tilt: 3.8, zoom: 1 } },
            { name: "대박의터", addr: "강원 춘천시 영서로 1786", panoid: 1195798040, pov: { pan: 63.49, tilt: 1.37, zoom: -1 } },
            { name: "대박찬스", addr: "경기 성남시 중원구 산성대로 4460", panoid: 1198939639, pov: { pan: 303.94, tilt: -2.44, zoom: 1 } },
            { name: "대박찬스", addr: "광주 북구 오치동 776-7", panoid: 1200654276, pov: { pan: 84.34, tilt: -1.70, zoom: -3 } },
            { name: "대박행진복권랜드", addr: "경기 파주시 금촌동 989-1 금촌프라자 107호", panoid: 1045548538, pov: { pan: 166.7, tilt: -1.1, zoom: 0 } },
            { name: "대야지복권", addr: "광주 남구 주월동 961-24", panoid: 1200569355, pov: { pan: 336.8, tilt: -0.3, zoom: 1 } },
            { name: "대영당안경원", addr: "부산 동래구 충렬대로237번길 9", panoid: 1202730682, pov: { pan: 292.71, tilt: 0.30, zoom: -3 } },
            { name: "대운복권", addr: "경기 성남시 중원구 성남대로 1149", panoid: 1199005721, pov: { pan: 247.83, tilt: 3.95, zoom: 1 } },
            { name: "대흥당", addr: "전북 정읍시 관통로 102", panoid: 1183542559, pov: { pan: 307.0, tilt: 0.9, zoom: 0 } },
            { name: "도깨비", addr: "경기 하남시 서하남로 136", panoid: 1173958844, pov: { pan: 178.97, tilt: 7.88, zoom: -3 } },
            { name: "도소매복권방", addr: "전남 광양시 광영동 759-4", panoid: 1205328614, pov: { pan: 108.57, tilt: 5.52, zoom: -3 } },
            { name: "동남슈퍼", addr: "전북 부안군 부안읍 동중리 130-5", panoid: 1182567764, pov: { pan: 337.8, tilt: 0.8, zoom: 0 } },
            { name: "동원슈퍼", addr: "광주 남구 월산5동 1053-22", panoid: 1200403334, pov: { pan: 228.78, tilt: 5.68, zoom: -3 } },
            { name: "동일통신", addr: "부산 해운대구 반여1동 1361-2", panoid: 1202252207, pov: { pan: 96.27, tilt: 11.77, zoom: -3 } },
            { name: "돼지복권명당", addr: "부산 기장군 철마면 임기리 365-1", panoid: 1201909627, pov: { pan: 325.76, tilt: 11.68, zoom: -3 } },
            { name: "둘리복권방", addr: "경기 시흥시 중심상가2길 12-6 한강1차101호", panoid: 1176042805, pov: { pan: 297.91, tilt: -0.61, zoom: -3 } },
            { name: "드림메드", addr: "경기 안산시 상록구 월피로 56 101호", panoid: 1204153598, pov: { pan: 120.5, tilt: -2.8, zoom: 0 } },
            { name: "따봉복권방", addr: "인천 부평구 부평4동 889-5", panoid: 1199330283, pov: { pan: 269.89, tilt: 4.38, zoom: -3 } },
            { name: "떴다GO 1등", addr: "경기 화성시 동탄반석로 172 1층 138호(동탄 파라곤점)", panoid: 1198012743, pov: { pan: 101.0, tilt: -4.0, zoom: 0 } },
            { name: "또와식품", addr: "서울 강서구 염창동 264-8", panoid: 1198500709, pov: { pan: 223.70, tilt: 0.06, zoom: -3 } },
            { name: "럭키복권방", addr: "서울 도봉구 창동 134-36 우림빌딩106", panoid: 1197759119, pov: { pan: 7.9, tilt: 3.7, zoom: 0 } },
            { name: "로또", addr: "충남 홍성군 홍성읍 오관리 311-5", panoid: 1161022501, pov: { pan: 200.38, tilt: 6.42, zoom: -1 } },
            { name: "로또 명당 가판점", addr: "서울 금천구 남부순환로 1390", panoid: 1198477792, pov: { pan: 154.59, tilt: -1.43, zoom: -3 } },
            { name: "로또25시", addr: "경기 수원시 권선구 권선동 1295-3 104호", panoid: 1199507269, pov: { pan: 91.76, tilt: 7.74, zoom: -3 } },
            { name: "로또로복권", addr: "전북 전주시 완산구 평화동2가 4729", panoid: 1172287937, pov: { pan: 293.02, tilt: -1.94, zoom: -3 } },
            { name: "로또매점", addr: "충남 당진시 송산면 유곡리 876-2", panoid: 1172172781, pov: { pan: 276.95, tilt: 4.01, zoom: 0 } },
            { name: "로또명당", addr: "경기 시흥시 신현로 21-1 101호", panoid: 1175428410, pov: { pan: 141.2, tilt: -1.0, zoom: 1 } },
            { name: "로또명당", addr: "인천 남구 문학동", panoid: 1200600347, pov: { pan: 254.27, tilt: 7.89, zoom: 0 } },
            { name: "로또복권", addr: "경북 김천시 신음동 462-24", panoid: 1165059457, pov: { pan: 21.12, tilt: -1.34, zoom: -3 } },
            { name: "로또복권", addr: "경기 화성시 송산면", panoid: 1198585012, pov: { pan: 181.41, tilt: 4.46, zoom: -1 } },
            { name: "로또복권 하대점", addr: "경남 진주시 하대동 188", panoid: 1193106643, pov: { pan: 82.61, tilt: 1.05, zoom: -3 } },
            { name: "로또복권방", addr: "경기 가평군 가평읍 읍내리 448-3", panoid: 1175611447, pov: { pan: 14.37, tilt: 5.66, zoom: -3 } },
            { name: "로또복권장항점", addr: "충남 서천군 장항읍 창선리 632-2", isClosed: true, customMessage: "현재 폐업 상태로 장항 지역의 다른 명당(1등명당 등)을 이용해 주세요." },
            { name: "로또복권짱", addr: "경기 용인시 처인구 남사읍 어비리 582-3", panoid: 1198953409, pov: { pan: 54.76, tilt: -1.02, zoom: -2 } },
            { name: "로또통신", addr: "경남 김해시 외동 1251-1 104호 (함박로101번길 22)", panoid: 1194388308, pov: { pan: 83.23, tilt: -3.87, zoom: -2 } },
            { name: "로또판매점", addr: "경기 포천시 신북면 가채리 23-2", panoid: 1176226525, pov: { pan: 97.77, tilt: 0.82, zoom: -2 } },
            { name: "로또판매점", addr: "충북 음성군 대소면 오산리 533-1", panoid: 1165303745, pov: { pan: 110.98, tilt: 4.60, zoom: -3 } },
            { name: "로또행운마트", addr: "경남 김해시 능동로 177 복권판매점", panoid: 1194480714, pov: { pan: 203.39, tilt: -2.23, zoom: 1 } },
            { name: "장미슈퍼", addr: "충남 부여군 계백로 265", panoid: 1178842351, pov: { pan: 265.99, tilt: 9.55, zoom: -3 } },
            { name: "까치복권방", addr: "경기 시흥시 중심상가로 326", panoid: 1176040884, pov: { pan: 216.52, tilt: -1.90, zoom: -3 } },
            { name: "로또복권", addr: "경기 평택시 원평로 55", panoid: 1197645349, pov: { pan: 221.40, tilt: 6.81, zoom: -2 } },
            { name: "복권나라", addr: "충북 청주시 상당구 상당로 9", panoid: 1169915133, pov: { pan: 266.59, tilt: 6.92, zoom: 2 } },
            { name: "세계로생활가전", addr: "서울 동작구 보라매로 104", panoid: 1197780011, pov: { pan: 92.63, tilt: 3.58, zoom: 0 } },
            { name: "도깨비방망이", addr: "전남 완도군 장보고대로 220", panoid: 1188939916, pov: { pan: 209.79, tilt: -1.13, zoom: 2 } },
            { name: "현대사", addr: "경기 성남시 분당구 미금일로 77", panoid: 1198797713, pov: { pan: 178.56, tilt: 1.66, zoom: 2 } },
            { name: "가로판매점", addr: "서울 서대문구 신촌로 103", panoid: 1198907641, pov: { pan: 114.23, tilt: -0.21, zoom: 0 } },
            { name: "알리바이금당점", addr: "전남 순천시 대석길 44", panoid: 1205278170, pov: { pan: 354.56, tilt: 10.79, zoom: 0 } },
            { name: "세원로또복권방", addr: "부산 수영구 수영로725번길 53", panoid: 1202601334, pov: { pan: 169.46, tilt: 6.04, zoom: -3 } },
            { name: "초월대박복권방", addr: "경기 광주시 경충대로 1252", panoid: 1203793227, pov: { pan: 46.47, tilt: 3.95, zoom: 0 } },
            { name: "경성식품", addr: "서울 동대문구 망우로21길 52", panoid: 1198205251, pov: { pan: 356.19, tilt: 0.06, zoom: 0 } },
            { name: "복권닷컴", addr: "강원 양양군 양양로 62", panoid: 1196252827, pov: { pan: 352.91, tilt: -4.50, zoom: 0 } },
            { name: "헬로마트", addr: "서울 도봉구 도봉로170길 8", panoid: 1197897753, pov: { pan: 166.06, tilt: 3.20, zoom: 2 } },
            { name: "로또명당", addr: "경기 시흥시 신현로 21-1", panoid: 1175428413, pov: { pan: 125.58, tilt: 0.25, zoom: 2 } },
            { name: "황금복권마트", addr: "경기 이천시 증신로325번길 5", panoid: 1174834139, pov: { pan: 202.46, tilt: -4.78, zoom: 3 } },
            { name: "로또", addr: "서울 중구 퇴계로86길 42", panoid: 1198788751, pov: { pan: 286.63, tilt: 0.96, zoom: -3 } },
            { name: "CU(군포덕산점)", addr: "경기 군포시 고산로250번길 32", panoid: 1175428530, pov: { pan: 27.11, tilt: -2.77, zoom: -2 } },
            { name: "롯데무역", addr: "부산 영도구 남항동1가 197-1번지 (꿈나무길 197)", panoid: 1202691794, pov: { pan: 108.98, tilt: 5.95, zoom: -3 } },
            { name: "마이마트", addr: "인천 서구 심곡동 302 한국상가 제1층 101호", panoid: 1199391535, pov: { pan: 182.2, tilt: -3.9, zoom: 0 }, customMessage: "기존 '이마트(인천 심곡)' 명칭으로 알려진 1등 4회 대박 명당입니다." },
            { name: "메가마트", addr: "경기 시흥시 정왕대로 64 메가쇼핑몰 1층 123호", panoid: 1176237881, pov: { pan: 20.5, tilt: -1.3, zoom: 1 } },
            { name: "광성슈퍼", addr: "경기 이천시 단월로", panoid: 1175073795, pov: { pan: 281.59, tilt: 0.26, zoom: -3 } },
            { name: "명성복권방", addr: "경기 화성시 경기대로 1043", panoid: 1198300197, pov: { pan: 207.00, tilt: -5.25, zoom: 3 } },
            { name: "명당마트", addr: "서울 강서구 양천로 91", panoid: 1198194653, pov: { pan: 70.47, tilt: -2.31, zoom: -3 } },
            { name: "명신사", addr: "서울 마포구 월드컵로 97", panoid: 1197543347, pov: { pan: 225.25, tilt: 6.55, zoom: -3 } },
            { name: "명진슈퍼", addr: "경기 의왕시 고천동 295-26", panoid: 1174117026, pov: { pan: 262.24, tilt: 5.16, zoom: -3 } },
            { name: "매물도복권점", addr: "경남 통영시 통영해안로 225-1 (서호동 177-336)", panoid: 1204407783, pov: { pan: 347.4, tilt: 5.4, zoom: 4 }, customMessage: "기존 '바다로또방(1등 3회)'의 당첨 기운을 이어받아 통합 운영 중인 명당입니다." },
            { name: "버스매표소", addr: "인천 부평구 부평대로 3 (부평동 549-39)", panoid: 1199209059, pov: { pan: 329.47, tilt: 1.58, zoom: -3 }, customMessage: "부평역 광장 가판대로 역사적인 당첨 기록을 보유한 명당입니다." },
            { name: "버스표판매소", addr: "경기 고양시 덕양구 화신로 76 샘터마을1단지 가판", panoid: 1203599815, pov: { pan: 212.0, tilt: 4.9, zoom: 0 }, customMessage: "행신동 샘터마을1단지 앞 가판대 명당입니다." },
            { name: "베스토아(용전2호)", addr: "대전 동구 동서대로 1689 복합터미널서관1층59호 (용전동 63-3)", panoid: 1201601961, pov: { pan: 248.2, tilt: 1.6, zoom: 0 }, customMessage: "동행복권 기록상 도로명/지번 주소 분산으로 인해 3+4회로 나뉘어 있던 총 7회 당첨의 전설적인 명당입니다." },
            { name: "보람복권방", addr: "울산 남구 화합로194번길 18-1 (삼산동 1567-6 우리들마트 내)", panoid: 1201998535, pov: { pan: 190.2, tilt: 0.9, zoom: 0 }, customMessage: "도로명/지번 주소 분산으로 4+4회로 나뉘어 있던 총 8회 당첨의 엄청난 명당입니다." },
            { name: "보경식품", addr: "서울 강북구 미아동 207-2", panoid: 1197862462, pov: { pan: 249.90, tilt: 1.60, zoom: -1 } },
            { name: "복권", addr: "경기 의정부시 태평로 75", panoid: 1174093159, pov: { pan: 277.0, tilt: 0.0, zoom: 0 } },
            { name: "복권나라", addr: "경북 포항시 북구 죽도동 140-9 (죽도로 9)", panoid: 1187494212, pov: { pan: 348.69, tilt: 12.87, zoom: -3 }, customMessage: "포항 죽도동의 명실상부한 1등 3회 배출 명당입니다." },
            { name: "복권나라", addr: "강원 원주시 평원로 23", panoid: 1196398296, pov: { pan: 277.97, tilt: 0.34, zoom: 0 } },
            { name: "복권나라", addr: "충북 증평군 증평읍 중앙로 15-3 (중동리 15-3)", panoid: 1184345935, pov: { pan: 303.17, tilt: -2.56, zoom: 1 } },
            { name: "복권나라", addr: "서울 성동구 용답중앙15길", panoid: 1198738844, pov: { pan: 125.91, tilt: 5.76, zoom: -1 }, customMessage: "기존 용답동 14-1번지(3회)에서 이전하여 총 5회 1등을 배출한 저력 있는 명당입니다." },
            { name: "복권나라", addr: "전남 여수시 중앙로 62", panoid: 1205476848, pov: { pan: 182.73, tilt: 3.14, zoom: -1 } },
            { name: "복권나라", addr: "인천 서구 석남동 586-2", panoid: 1200085676, pov: { pan: 180.1, tilt: 2.3, zoom: 0 } },
            { name: "복권명당", addr: "경기 안성시 공도읍 승두길 62 (승두리 60-129)", panoid: 1176200480, pov: { pan: 171.58, tilt: 1.98, zoom: -1 }, customMessage: "지번/도로명 주소 분산 기록을 포함하여 총 4회 1등을 배출한 명당입니다." },
            { name: "복권명당", addr: "경북 경산시 경안로 214 (중방동 436-11)", panoid: 1187314576, pov: { pan: 30.42, tilt: 4.74, zoom: 2 } },
            { name: "복권명당", addr: "대전 중구 목중로 47 (중촌동 21-18)", panoid: 1201428533, pov: { pan: 216.8, tilt: 0.7, zoom: 0 }, customMessage: "지번/도로명 주소 분산 기록을 포함하여 총 4회 1등을 배출한 명당입니다." },
            { name: "복권방", addr: "경기 수원시 팔달구 인계로 213 (인계동 1037-2)", panoid: 1199811682, pov: { pan: 176.89, tilt: 1.16, zoom: -2 }, customMessage: "지번/도로명 주소 분산 기록을 포함하여 총 4회 1등을 배출한 인계동 명당입니다." },
            { name: "복권방", addr: "서울 구로구 구로동 409-80 (구로동로35길 6)", panoid: 1198456741, pov: { pan: 299.0, tilt: 3.0, zoom: 3 }, isClosed: true, customMessage: "과거 1등을 3회 배출했으나 현재는 폐점된 매장입니다." },
            { name: "복권방", addr: "경기 하남시 신장로 122", panoid: 1173490651, pov: { pan: 27.4, tilt: -6.5, zoom: 0 }, customMessage: "하남 신장동의 대표 명당으로, 인근 폐점된 지점(2회)과 합산하여 총 6회 1등을 배출한 저력 있는 곳입니다. LG U+ 매장 내에 위치하고 있습니다." },
            { name: "CU 원주관설점", addr: "강원 원주시 관설동 1702-1 (나비허리길 160)", panoid: 1195742104, pov: { pan: 172.47, tilt: 3.39, zoom: -3 }, customMessage: "기존 '복권방'의 당첨 이력을 승계하여 운영 중인 편의점 명당입니다." },
            { name: "복권백화점", addr: "경기 여주시 세종로 41", panoid: 1174873101, pov: { pan: 132.31, tilt: 2.55, zoom: 2 } },
            { name: "복권사랑", addr: "경기 양주시 평화로 1421 (덕계동 462-2)", panoid: 1204107039, pov: { pan: 112.71, tilt: 1.11, zoom: 1 } },
            { name: "복권전문점", addr: "대전 유성구 계룡로 132번길 10 (봉명동 568-4)", panoid: 1201068426, pov: { pan: 205.90, tilt: 4.45, zoom: -3 } },
            { name: "복권천국", addr: "부산 서구 구덕로 207-1 (부민동2가 10-8)", panoid: 1202160948, pov: { pan: 215.57, tilt: 6.67, zoom: 0 } },
            { name: "복권천국방", addr: "서울 마포구 어울마당로 125 (서교동 480-1)", panoid: 1197902493, pov: { pan: 172.06, tilt: 8.06, zoom: 0 } },
            { name: "복돼지복권방", addr: "전북 익산시 선화로1길 4 (배산시티프라자 107호)", panoid: 1179805782, pov: { pan: 16.3, tilt: 2.2, zoom: 5 }, customMessage: "지번/도로명 및 중복 주소 기록을 통합하여 총 4회 1등을 배출한 익산 명당입니다." },
            { name: "부강 돈벼락", addr: "경남 양산시 물금로 41 (물금리 800-5, 양우내안애5차 상가 108호)", panoid: 1204485832, pov: { pan: 44.5, tilt: -1.0, zoom: 3 }, customMessage: "양산 물금읍의 숨은 명당으로 로또 1등 3회 배출 기록을 보유하고 있습니다." },
            { name: "부자랑", addr: "서울 성동구 둘레15길 23", panoid: 1198725466, pov: { pan: 247.57, tilt: 5.20, zoom: -3 } },
            { name: "북부슈퍼", addr: "경기 의정부시 가능로125번길 22", panoid: 1174088094, pov: { pan: 46.90, tilt: 10.25, zoom: -3 } },
            { name: "돈벼락", addr: "경기 부천시 범안로 220 제근린생활시설2동 1층 103호", panoid: 1203479413, pov: { pan: 335.2, tilt: 4.8, zoom: 0 } },
            { name: "돈벼락맞는곳", addr: "부산 사상구 낙동대로 910 마트월드 A-160호", panoid: 1202359872, pov: { pan: 90.17, tilt: 4.12, zoom: 0 } },
            { name: "돈벼락맞는곳", addr: "대전 서구 복수남로 16", panoid: 1200853943, pov: { pan: 42.10, tilt: 1.51, zoom: -3 } },
            { name: "돈벼락맞는곳", addr: "경남 김해시 한림면 신천리 980-7", panoid: 1194446892, pov: { pan: 206.04, tilt: 4.71, zoom: 0 } },
            { name: "돈벼락복권방", addr: "대구 북구 동변동 686", panoid: 1201176065, pov: { pan: 79.5, tilt: 0.5, zoom: 0 } },
            { name: "NBA(엔비에이)", addr: "운서동 2803-1 128호", panoId: 1199042496, pov: { pan: 185.43, tilt: -3.07, zoom: 2 } },
            { name: "헬로마트", addr: "서울 도봉구 도봉2동 89-148", panoId: 1197897753, pov: { pan: 137.1, tilt: 6.5, zoom: 2 } },
            { name: "북문복권방", addr: "정조로 927-1", panoId: 1199757912, pov: { pan: 147.1, tilt: 4.8, zoom: 2 } },
            { name: "로또", addr: "서울 중구 신당동", panoId: 1198788751, pov: { pan: 276.93, tilt: 5.46, zoom: -3 } },
            { name: "데이앤나잇", addr: "서울 성북구 종암동", panoId: 1198236406, pov: { pan: 59.17, tilt: 4.90, zoom: -1 } },
            { name: "초월대박복권방", addr: "경기 광주시 초월읍", panoId: 1203793226, pov: { pan: 46.93, tilt: 0.32, zoom: -1 } },
            { name: "25시슈퍼", addr: "경남 창원시 마산회원구", panoId: 1204402491, pov: { pan: 7.70, tilt: -1.92, zoom: -3 } },
            { name: "25시슈퍼", addr: "경기 시흥시 정왕동", panoId: 1176030803, pov: { pan: 307.08, tilt: 2.52, zoom: 0 } },
            { name: "CU(대림중앙점)", addr: "서울 영등포구 대림3동", panoId: 1198470102, pov: { pan: 287.22, tilt: 4.36, zoom: 1 } },
            { name: "GS25(두정메트로점)", addr: "충남 천안시 서북구", panoId: 1195535897, pov: { pan: 4.40, tilt: -3.16, zoom: -3 } },
            { name: "GS25(양산혜인점)", addr: "경남 양산시 평산동", panoId: 1204592950, pov: { pan: 284.55, tilt: -2.89, zoom: -3 } },
            { name: "GS25(종로낙원)", addr: "서울 종로구 낙원동", panoId: 1198436368, pov: { pan: 247.55, tilt: 6.34, zoom: -3 } },
            { name: "GS25(중촌현대)", addr: "대전 중구 중촌동", panoId: 1201489199, pov: { pan: 314.11, tilt: -0.33, zoom: -3 } },
            { name: "G마트", addr: "서울 영등포구 디지털로", panoId: 1198746873, pov: { pan: 272.22, tilt: 7.62, zoom: 0 } },
            { name: "HX복권방", addr: "경기 이천시 부발읍", panoId: 1175067769, pov: { pan: 81.37, tilt: -0.54, zoom: 0 } },
            { name: "NBA(엔비에이)", addr: "인천 중구 신도시남로142번길", panoId: 1199042496, pov: { pan: 163.15, tilt: -3.80, zoom: 1 } },
            { name: "NG24", addr: "경북 칠곡군 북중리3길", panoId: 1166761988, pov: { pan: 317.63, tilt: 0.25, zoom: -3 } },
            { name: "가판14호", addr: "서울 중구 퇴계로", panoId: 1198729502, pov: { pan: 325.62, tilt: 2.13, zoom: -3 } },
            { name: "금강종합공구", addr: "경기 김포시 대곶면", panoId: 1203805177, pov: { pan: 152.44, tilt: 6.16, zoom: 1 } },
            { name: "금곡로", addr: "경기 수원시 권선구", panoId: 1199869934, pov: { pan: 223.14, tilt: -10.18, zoom: 1 } },
            { name: "김포로또", addr: "경기 김포시 사우동", panoId: 1203803036, pov: { pan: 30.03, tilt: 0.32, zoom: 1 } },
            { name: "나눔로또 판교역점", addr: "경기 성남시 분당구 대왕판교로606번길 39", panoid: 1199366275, pov: { pan: 355.75, tilt: -3.62, zoom: 1 }, customMessage: "건물 내부에 매장이 있습니다" },
            { name: "노다지복권", addr: "강원 횡성군 문정로", panoId: 1197181543, pov: { pan: 217.60, tilt: 1.34, zoom: -1 } },
            { name: "다모아복권", addr: "서울 구로구 오류동", panoId: 1198581650, pov: { pan: 54.87, tilt: 2.77, zoom: -3 } },
            { name: "다모아복권방", addr: "서울 구로구 오류동", panoId: 1198548447, pov: { pan: 256.07, tilt: 0.72, zoom: -3 } },
            { name: "대박스타", addr: "인천 미추홀구 경인로", panoId: 1199708556, pov: { pan: 180.27, tilt: 0.72, zoom: -1 } },
            { name: "대박찬스", addr: "충북 청주시 흥덕구", panoId: 1170563610, pov: { pan: 247.36, tilt: -0.69, zoom: -1 } },
            { name: "대성기획", addr: "경기 용인시 기흥구 구성로", panoId: 1199504553, pov: { pan: 11.62, tilt: 0.18, zoom: -3 } },
            { name: "대원슈퍼마켓", addr: "부산 수영구 광안2동", panoId: 1202817759, pov: { pan: 102.41, tilt: 4.05, zoom: -3 } },
            { name: "돈벼락맞는곳", addr: "부산 기장군 읍내로", panoId: 1162339595, pov: { pan: 354.91, tilt: -2.05, zoom: -3 } },
            { name: "동원복권", addr: "경남 양산시 북정동", panoId: 1204826032, pov: { pan: 118.64, tilt: 0.81, zoom: -3 } },
            { name: "드림", addr: "경기 수원시 권선구", panoid: 1200109952, pov: { pan: 311.37, tilt: 0.30, zoom: 0 } },
            { name: "드림마트", addr: "인천 서구 검단로", panoId: 1198835640, pov: { pan: 148.68, tilt: 2.64, zoom: -3 } },
            { name: "로또", addr: "경기 포천시 죽엽산로196번길", panoId: 1175927131, pov: { pan: 316.68, tilt: -1.36, zoom: -3 } },
            { name: "로또(파발마점)", addr: "경기 시흥시 정왕동", panoId: 1175870702, pov: { pan: 114.75, tilt: -1.36, zoom: -3 } },
            { name: "로또대박", addr: "세종 장척로 571", panoId: 1200779340, pov: { pan: 21.15, tilt: 1.86, zoom: -3 } },
            { name: "로또대박", addr: "경기 부천시 석천로177번길", panoId: 1203625174, pov: { pan: 190.23, tilt: -5.06, zoom: -3 } },
            { name: "로또명당해미점", addr: "충남 서산시 해미면", panoId: 1177266091, pov: { pan: 261.83, tilt: 4.10, zoom: -3 } },
            { name: "로또복권방", addr: "충남 당진시 당진읍", panoId: 1174017431, pov: { pan: 349.10, tilt: 2.80, zoom: -3 } },
            { name: "로또복권하대점", addr: "경남 진주시 하대동", panoId: 1193106643, pov: { pan: 84.77, tilt: 1.40, zoom: -3 } },
            { name: "로또천국", addr: "충북 충주시 칠금동", panoId: 1164453210, pov: { pan: 296.39, tilt: -0.41, zoom: 0 } },
            { name: "로터리편의마트", addr: "경북 포항시 북구", panoId: 1187245253, pov: { pan: 37.52, tilt: 4.06, zoom: -3 } },
            { name: "마두5번출구가판로또", addr: "경기 고양시 일산동구", panoId: 1203614425, pov: { pan: 72.37, tilt: 0.55, zoom: 1 } },
            { name: "명당", addr: "경남 진주시 동부로", panoId: 1193074745, pov: { pan: 108.48, tilt: -6.44, zoom: -1 } },
            { name: "묵동식품", addr: "서울 중랑구 동일로", panoId: 1198448343, pov: { pan: 224.74, tilt: 2.27, zoom: 1 } },
            { name: "버스표가판점", addr: "경기 안양시 동안구", panoId: 1203300471, pov: { pan: 234.49, tilt: -8.46, zoom: -1 } },
            { name: "베스트올수성점", addr: "전북 정읍시 수성동", panoId: 1183495363, pov: { pan: 211.63, tilt: 15.04, zoom: -3 } },
            { name: "복권나라", addr: "서울 관악구 은천로", panoId: 1198290120, pov: { pan: 330.0, tilt: 8.0, zoom: 1 } },
            { name: "복권마을", addr: "서울 구로구 구로동로", panoId: 1198161434, pov: { pan: 75.40, tilt: 2.67, zoom: -3 } },
            { name: "복권방", addr: "부산 사하구 장림동", panoId: 1202461052, pov: { pan: 33.37, tilt: -4.08, zoom: -3 } },
            { name: "복권세상", addr: "전남 목포시 청호로", panoId: 1192169730, pov: { pan: 228.46, tilt: 5.41, zoom: -2 } },
            { name: "복권세상", addr: "경기 여주시 우암로", panoId: 1174843105, pov: { pan: 89.62, tilt: 2.70, zoom: -2 } },
            { name: "복권파는집", addr: "경남 창원시 마산회원구", panoId: 1204721909, pov: { pan: 319.58, tilt: -6.57, zoom: -2 } },
            { name: "복돼지복권방", addr: "경기 화성시 3.1만세로", panoId: 1196772296, pov: { pan: 338.50, tilt: 1.21, zoom: -2 } },
            { name: "본스튜디오", addr: "제주 제주시 하귀로", panoId: 1181077460, pov: { pan: 338.03, tilt: 0.61, zoom: -2 } },
            { name: "부자복권방", addr: "전북 군산시 대명동", panoId: 1172510553, pov: { pan: 57.92, tilt: -0.16, zoom: -2 } },
            { name: "삼삼마트", addr: "경남 진주시 봉곡동", panoId: 1192627365, pov: { pan: 159.63, tilt: 3.61, zoom: -3 } },
            { name: "서재강변로또", addr: "대구 달성군 다사읍", panoId: 1200883303, pov: { pan: 116.21, tilt: -2.75, zoom: -3 } },
            { name: "서정천하명당", addr: "경기 평택시 서정동", panoId: 1198410230, pov: { pan: 79.3, tilt: 5.2, zoom: 0 } },
            { name: "성심상회", addr: "경북 포항시 북구 불종로", panoId: 1186982434, pov: { pan: 198.8, tilt: -6.1, zoom: 0 } },
            { name: "성호복권방", addr: "대전 대덕구 신일동로", panoId: 1201128527, pov: { pan: 19.99, tilt: 4.58, zoom: -3 } },
            { name: "세븐일레븐 홍익점", addr: "경기 안성시 종합운동장로", panoId: 1176123645, pov: { pan: 325.1, tilt: 0.9, zoom: -1 } },
            { name: "세종로또방", addr: "세종 용포로 32", panoId: 1200677275, pov: { pan: 81.66, tilt: 5.68, zoom: -3 } },
            { name: "수퍼복권대박", addr: "인천 연수구 용담로", panoId: 1200644068, pov: { pan: 201.2, tilt: -4.2, zoom: 0 } },
            { name: "신불당로또", addr: "충남 천안시 서북구", panoId: 1195219571, pov: { pan: 267.81, tilt: -0.01, zoom: 0 } },
            { name: "신영슈퍼", addr: "서울 강남구 광평로51길", panoId: 1198825857, pov: { pan: 11.28, tilt: -0.54, zoom: 0 } },
            { name: "씨스페이스 어방점", addr: "경남 김해시 인제로170번길 15-6 편의점 내", panoid: 1195018021, pov: { pan: 46.35, tilt: 5.03, zoom: 1 } },
            { name: "씨유 대전반석역점", addr: "대전 유성구 반석로", panoId: 1200979469, pov: { pan: 21.38, tilt: 1.42, zoom: 0 } },
            { name: "아이러브마트복권방", addr: "울산 중구 유곡로", panoId: 1202037956, pov: { pan: 166.5, tilt: 1.3, zoom: -1 } },
            { name: "알리바이", addr: "광주 광산구 신가동", panoId: 1199874247, pov: { pan: 46.58, tilt: -6.28, zoom: -3 } },
            { name: "오늘의로또", addr: "경기 오산시 권리사로", panoId: 1198544061, pov: { pan: 224.2, tilt: 3.3, zoom: 0 } },
            { name: "용꿈돼지꿈복권방", addr: "경기 시흥시 하중로", panoId: 1175674861, pov: { pan: 75.71, tilt: -6.45, zoom: 1 } },
            { name: "우일", addr: "서울 송파구 마천2동", panoId: 1198540869, pov: { pan: 359.88, tilt: 1.39, zoom: 2 } },
            { name: "원당역복권방", addr: "경기 고양시 덕양구", panoId: 1203875563, pov: { pan: 39.96, tilt: -0.78, zoom: -1 } },
            { name: "인생대역전", addr: "인천 계양구 임학동", panoId: 1198902079, pov: { pan: 301.04, tilt: 0.71, zoom: -1 } },
            { name: "자수정슈퍼", addr: "전북 전주시 완산구", panoId: 1172061409, pov: { pan: 143.41, tilt: -2.21, zoom: -1 } },
            { name: "장미슈퍼", addr: "충남 부여군 부여읍", panoId: 1178842351, pov: { pan: 265.2, tilt: 0.1, zoom: -1 } },
            { name: "제이복권방", addr: "서울 종로구 종로5가", panoId: 1197815068, pov: { pan: 358.97, tilt: -5.13, zoom: -3 } },
            { name: "종로3가1호선역2번출구가로판매점82호", addr: "서울 종로구 종로3가", panoId: 1198163888, pov: { pan: 238.8, tilt: 0.6, zoom: -1 } },
            { name: "종합복권방", addr: "전남 해남군 해남읍", panoId: 1189205617, pov: { pan: 162.87, tilt: -3.96, zoom: -3 } },
            { name: "주엽역 로또판매점", addr: "경기 고양시 일산서구", panoId: 1203613079, pov: { pan: 227.60, tilt: -1.98, zoom: -1 } },
            { name: "주택복권방", addr: "강원 원주시 우산초교길", panoId: 1195999144, pov: { pan: 209.61, tilt: 1.36, zoom: -3 } },
            { name: "주택복권방", addr: "경기 용인시 수지구", panoId: 1199750334, pov: { pan: 142.54, tilt: 0.54, zoom: -1 } },
            { name: "진우복권", addr: "부산 연제구 월드컵대로", panoId: 1202681433, pov: { pan: 140.83, tilt: -14.59, zoom: -3 } },
            { name: "진우행운복권방", addr: "경기 광주시 도척로", panoId: 1203185125, pov: { pan: 269.1, tilt: 1.7, zoom: 0 } },
            { name: "천하명당", addr: "경기 평택시 탄현로", panoId: 1198300869, pov: { pan: 95.49, tilt: 2.73, zoom: 0 } },
            { name: "천하명당복권", addr: "대구 북구 칠곡중앙대로", panoId: 1201202732, pov: { pan: 280.77, tilt: 8.47, zoom: 0 } },
            { name: "천하명당복권", addr: "대구 북구 관음동", panoId: 1201464296, pov: { pan: 208.77, tilt: 11.18, zoom: -3 } },
            { name: "천하명당복권방", addr: "경기 수원시 팔달구", panoId: 1200112414, pov: { pan: 58.24, tilt: 4.22, zoom: 1 } },
            { name: "천하명당복권방", addr: "경남 거제시 옥포1동", panoId: 1204368034, pov: { pan: 81.98, tilt: 0.07, zoom: 1 } },
            { name: "천하명당복권방", addr: "충남 홍성군 홍성읍", panoId: 1161022469, pov: { pan: 191.39, tilt: 10.32, zoom: 1 } },
            { name: "탑로또", addr: "경남 거제시 상동동(상문동)", panoId: 1204694341, pov: { pan: 210.88, tilt: -2.11, zoom: 2 } },
            { name: "팡팡복권방", addr: "충북 진천군 광혜원면", panoId: 1185181826, pov: { pan: 116.28, tilt: 6.65, zoom: -1 } },
            { name: "패밀리복권방", addr: "경기 남양주시 늘을1로16번길", panoId: 1203140248, pov: { pan: 243.5, tilt: -1.1, zoom: 0 } },
            { name: "편의점사랑", addr: "서울 강서구 곰달래로25길", panoId: 1198753892, pov: { pan: 147.44, tilt: -2.70, zoom: -3 } },
            { name: "프로토베팅샵", addr: "부산 중구 국제시장2길", panoId: 1132643336, pov: { pan: 240.67, tilt: 2.55, zoom: -3 } },
            { name: "하늘과바다", addr: "인천 부평구 부개동", panoId: 1199223112, pov: { pan: 0.36, tilt: -0.01, zoom: -2 } },
            { name: "하당복권방", addr: "전남 목포시 옥암동", panoId: 1192600420, pov: { pan: 304.76, tilt: 1.45, zoom: -3 } },
            { name: "하영", addr: "인천 서구 청라에메랄드로", panoId: 1199762293, pov: { pan: 254.5, tilt: -13.8, zoom: 1 } },
            { name: "해수로또", addr: "충북 청주시 상당구 산성로", panoid: 1168821889, pov: { pan: 87.7, tilt: -8.7, zoom: 0 } },
            { name: "행운방", addr: "경기 용인시 기흥구 보정동", panoid: 1194380962, pov: { pan: 99.2, tilt: 3.0, zoom: -1 } },
            { name: "행운복권", addr: "충북 제천시 의림동", panoid: 1184953799, pov: { pan: 14.56, tilt: 5.01, zoom: 0 } },
            { name: "행운복권", addr: "경기 군포시 대야미동", panoid: 1175680167, pov: { pan: 302.4, tilt: 7.5, zoom: -1 } },
            { name: "행운복권방", addr: "부산 중구 남포동5가", panoId: 1202742263, pov: { pan: 162.33, tilt: -1.85, zoom: -2 } },
            { name: "행운복권방", addr: "경기 의정부시 용현동", panoId: 1174558837, pov: { pan: 255.27, tilt: -1.13, zoom: -3 } },
            { name: "행운복권방", addr: "강원 인제군 북면", panoId: 1196203792, pov: { pan: 216.8, tilt: -5.2, zoom: 0 } },
            { name: "행운을주는사람들", addr: "충북 충주시 연수동", panoid: 1165060593, pov: { pan: 232.92, tilt: 3.33, zoom: -3 } },
            { name: "형제상회", addr: "대전 서구 용문동", panoId: 1201235032, pov: { pan: 231.57, tilt: 11.75, zoom: -3 } },
            { name: "현대사", addr: "경기 성남시 분당구 구미동 144-1 102호", panoId: 1199011246, pov: { pan: 359.56, tilt: 1.25, zoom: -3 } },
            { name: "행운복권방", addr: "서울 도봉구 창동", panoId: 1197759123, pov: { pan: 334.7, tilt: -0.9, zoom: 0 } },
            { name: "천하명당초량점", addr: "부산 동구 중앙대로221번길 3", panoid: 1202441096, pov: { pan: 189.21, tilt: 7.73, zoom: -3 } },
            { name: "선경로또", addr: "충북 제천시용두대로 59", panoid: 1185117093, pov: { pan: 309.50, tilt: -2.42, zoom: 1 } },
            { name: "바로전산", addr: "경기 광명시 오리로 1000", panoid: 1203338330, pov: { pan: 20.22, tilt: 0.87, zoom: 1 } },
            { name: "가로판매점", addr: "서울 금천구 시흥대로 480 가판", panoid: 1198112467, pov: { pan: 47.89, tilt: 1.89, zoom: 2 } },
            { name: "행운복권", addr: "경북 구미시 야은로 763", panoid: 1166471666, pov: { pan: 11.23, tilt: 2.02, zoom: 0 } },
            { name: "행복미니슈퍼", addr: "경기 부천시 원미구", panoId: 1203727268, pov: { pan: 6.0, tilt: 2.8, zoom: 5 } },
            { name: "행복복권방", addr: "경남 창원시 의창구", panoId: 1205303190, pov: { pan: 306.09, tilt: 0.16, zoom: 2 } },
            { name: "소답시내버스매표소", addr: "경남 창원시 의창구 의안로2번길 17 가판", panoid: 1204901032, pov: { pan: 343.63, tilt: -0.00, zoom: 1 } },
            { name: "행운의집", addr: "서울 강동구 구천면로 222", panoid: 1198592857, pov: { pan: 133.80, tilt: 4.49, zoom: 1 } },
            { name: "금집복권", addr: "광주 북구 첨단연신로108번길 134", panoid: 1200811114, pov: { pan: 87.22, tilt: -1.84, zoom: -1 } },
            { name: "1등복권방", addr: "울산 울주군 동문길 84", panoid: 1201776500, pov: { pan: 254.00, tilt: 1.12, zoom: -1 } },
            { name: "대동도기상사", addr: "경북 영천시 금완로 30", panoid: 1200482286, pov: { pan: 178.75, tilt: 12.90, zoom: -1 } },
            { name: "행운을주는로또판매점", addr: "경기 안산시 단원구 초지로 90", panoid: 1204019935, pov: { pan: 93.36, tilt: -0.99, zoom: 3 } },
            { name: "나눔로또 판교역점", addr: "경기 성남시 분당구 대왕판교로606번길 39", panoid: 1199366275, pov: { pan: 355.75, tilt: -3.62, zoom: 1 }, customMessage: "건물 내부에 매장이 있습니다" },
            { name: "복권왕국", addr: "전남 여수시 여수산단로 48 1층101호", panoid: 1205610765, pov: { pan: 114.04, tilt: 0.85, zoom: 1 } },
            { name: "청룡마트", addr: "충남 천안시 동남구 풍세로 1010-31", panoid: 1194562374, pov: { pan: 134.12, tilt: 4.56, zoom: 1 } },
            { name: "돈벼락맞는곳", addr: "경남 김해시 김해대로 2793", panoid: 1194076312, pov: { pan: 42.87, tilt: 3.36, zoom: 2 } },
            { name: "남평로또점", addr: "전남 나주시 남평1로 12", panoid: 1191039911, pov: { pan: 186.94, tilt: 4.05, zoom: 1 } },
            { name: "불국사명당복권", addr: "경북 경주시 산업로 3033", panoid: 1187507967, pov: { pan: 229.11, tilt: -4.51, zoom: 1 } },
            { name: "잘찍어로또방", addr: "경기 평택시 안현로서5길 62", panoid: 1197880799, pov: { pan: 114.08, tilt: -4.66, zoom: 1 } },
            { name: "로또복권판매도통점", addr: "전북 남원시 용성로 232", panoid: 1181200294, pov: { pan: 253.83, tilt: 0.40, zoom: 1 } },
            { name: "해뜰날", addr: "경기 동두천시 중앙로 134-30", panoid: 1175647022, pov: { pan: 173.89, tilt: 2.93, zoom: 1 } },
            { name: "행운방", addr: "경기 용인시 기흥구 보정동", panoId: 1194380962, pov: { pan: 99.2, tilt: 3.0, zoom: -1 } },
            { name: "행운복권", addr: "충북 제천시 의림동", panoId: 1184953799, pov: { pan: 14.56, tilt: 5.01, zoom: 0 } },
            { name: "행운복권", addr: "경기 군포시 대야미동", panoId: 1175680167, pov: { pan: 302.4, tilt: 7.5, zoom: -1 } },
            { name: "행운복권방", addr: "부산 중구 남포동5가", panoId: 1202742263, pov: { pan: 162.33, tilt: -1.85, zoom: -2 } },
            { name: "행운복권방", addr: "경기 의정부시 용현동", panoId: 1174558837, pov: { pan: 255.27, tilt: -1.13, zoom: -3 } },
            { name: "행운복권방", addr: "강원 인제군 북면", panoId: 1196203792, pov: { pan: 216.8, tilt: -5.2, zoom: 0 } },
            { name: "행운을주는사람들", addr: "충북 충주시 연수동", panoId: 1165060593, pov: { pan: 232.92, tilt: 3.33, zoom: -3 } },
            { name: "형제상회", addr: "대전 서구 용문동", panoId: 1201235032, pov: { pan: 231.57, tilt: 11.75, zoom: -3 } },
            { name: "현대사", addr: "경기 성남시 분당구 구미동 144-1 102호", panoId: 1199011246, pov: { pan: 359.56, tilt: 1.25, zoom: -3 } },
            { name: "행운복권방", addr: "서울 도봉구 창동", panoId: 1197759123, pov: { pan: 334.7, tilt: -0.9, zoom: 0 } },
            { name: "천하명당초량점", addr: "부산 동구 중앙대로221번길 3", panoid: 1202441096, pov: { pan: 189.21, tilt: 7.73, zoom: -3 } },
            { name: "선경로또", addr: "충북 제천시용두대로 59", panoid: 1185117093, pov: { pan: 309.50, tilt: -2.42, zoom: 1 } },
            { name: "바로전산", addr: "경기 광명시 오리로 1000", panoid: 1203338330, pov: { pan: 20.22, tilt: 0.87, zoom: 1 } },
            { name: "가로판매점", addr: "서울 금천구 시흥대로 480 가판", panoid: 1198112467, pov: { pan: 47.89, tilt: 1.89, zoom: 2 } },
            { name: "포시즌마전점", addr: "인천 서구 완정로10번길", panoid: 1199590585, pov: { pan: 103.21, tilt: 1.73, zoom: -3 } },
            { name: "로또판매점", addr: "경기 고양시 일산동구", panoid: 1203808276, pov: { pan: 156.30, tilt: 1.44, zoom: -1 }, customMessage: "건물 내부에 매장이 있습니다" },
        ];


        function handleFileSelect(event) {
            const file = event.target.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = function (e) {
                try {
                    const data = JSON.parse(e.target.result);
                    processLoadedData(data);
                    document.getElementById('manualLoader').style.display = 'none';
                    alert('데이터를 성공적으로 불러왔습니다! (' + data.length + '건)');
                } catch (err) {
                    alert('파일 형식이 잘못되었습니다: ' + err.message);
                }
            };
            reader.readAsText(file);
        }

        function processLoadedData(data) {
            allData = data;

            // Calculate win count per shop (Name + Address)
            const shopWins = {};
            data.forEach(item => {
                const key = (item.n || '').trim() + '|' + (item.a || '').trim();
                shopWins[key] = (shopWins[key] || 0) + 1;
            });
            // Attach individual shop win count to each record
            let highWinCount = 0;
            data.forEach(item => {
                const key = (item.n || '').trim() + '|' + (item.a || '').trim();
                item.totalWins = shopWins[key];
                if (item.totalWins >= 5) highWinCount++;
            });
            console.log('Grouped Shops:', Object.keys(shopWins).length);
            console.log('Records with 5+ wins:', highWinCount);

            document.getElementById('totalDataCount').innerText = data.length.toLocaleString();
            if (data.length > 0) {
                const rounds = data.map(d => d.r);
                const maxR = Math.max(...rounds);
                const minR = Math.min(...rounds);

                // Force max round to 1211 as per user request (User Request: 1211)
                const targetMax = Math.max(maxR, 1211);

                document.getElementById('maxRound').value = targetMax;
                document.getElementById('minRound').value = Math.max(1, targetMax - 9);
            }

            applyFilters();

            // Initial load of recent rounds
            const initialMax = parseInt(document.getElementById('maxRound').value) || 1211;
            updateRecentRounds(initialMax);

            // --- Add Real-time Event Listeners ---
            const filterIds = [
                'minRound', 'maxRound',
                'freq5', 'freq3', 'freq1',
                'methodAuto', 'methodManual', 'methodSemi',
                'excludeClosed'
            ];

            filterIds.forEach(id => {
                const el = document.getElementById(id);
                if (!el) return;

                const eventType = el.type === 'checkbox' ? 'change' : 'input';
                el.addEventListener(eventType, () => {
                    applyFilters();

                    // Special case: if maxRound changes, also update the bottom dashboard
                    if (id === 'maxRound') {
                        const val = parseInt(el.value);
                        if (!isNaN(val)) updateRecentRounds(val);
                    }
                });
            });
        }

        window.onload = async function () {
            if (typeof kakao === 'undefined' || typeof kakao.maps === 'undefined') {
                handleScriptError();
                return;
            }

            const mapContainer = document.getElementById('map');
            const mapOption = { center: new kakao.maps.LatLng(36.2683, 127.6358), level: 12 };
            map = new kakao.maps.Map(mapContainer, mapOption);

            // Close InfoWindow when clicking on map background
            // Close InfoWindow & Toasts when clicking on map background
            kakao.maps.event.addListener(map, 'click', function () {
                // 1. Close InfoWindow
                if (currentInfoWindow) {
                    currentInfoWindow.close();
                    currentInfoWindow = null;
                    document.body.classList.remove('iw-open'); // Restore UI
                }

                // 2. Close All Toasts (including "Nearby Shops")
                closeAllToasts();

                // 3. Close Side Nav if open (Optional, but good UX)
                closeNav();
            });

            clusterer = new kakao.maps.MarkerClusterer({
                map: map, averageCenter: true, minLevel: 10,
                styles: [{
                    width: '40px', height: '40px', background: 'rgba(211, 47, 47, 0.8)',
                    color: '#fff', textAlign: 'center', lineHeight: '40px',
                    borderRadius: '20px', fontWeight: 'bold'
                }]
            });

            await loadData();

            // --- Add Map Idle Listener for "Nearby Sync" (Fix iPhone/Mobile desync issue) ---
            kakao.maps.event.addListener(map, 'idle', function () {
                const toast = document.getElementById('nearby-shops-toast');
                if (toast) {
                    const center = map.getCenter();
                    // Update list based on map center, but don't re-pan (prevent infinite loop)
                    findNearestShop(center.getLat(), center.getLng(), "지도 중심", false);
                }
            });

            // Auto-reflect GPS location on initial load (User Request)
            console.log('Initiating automatic GPS request on load...');
            requestMyLocation();
        };

        async function loadData() {
            const countEl = document.getElementById('totalDataCount');
            console.log('Loading data...');
            const cacheBuster = '?v=' + Date.now();

            try {
                // Using simple          pat         are most reliable on GitHub Pages
                const [lottoData, historyData] = await Promise.all([
                    fetch('https://integral81.github.io/lottomap/lotto_data.json' + cacheBuster).then(res => {
                        if (!res.ok) throw new Error('Data file not found (404)');
                        return res.json();
                    }),
                    fetch('https://integral81.github.io/lottomap/lotto_history.json' + cacheBuster).then(res => {
                        if (!res.ok) throw new Error('History file not found (404)');
                        return res.json();
                    })
                ]);

                window.lottoHistory = historyData;
                processLoadedData(lottoData);
            } catch (err) {
                console.error('Data load failed:', err);
                countEl.innerHTML = `<span style="color:red; font-size:11px;">로드 실패</span>`;
                alert('데이터 파일 로드 중 에러가 발생했습니다.\n\n주소 끝에 / 를 붙였는지 확인해 주세요.\n(예: k-inov.com/lottomap/)');
            }
        }

        // --- Advanced Prediction Algorithm ---
        let globalWeights = null; // Calculated once on load
        let lastRecommendedNumbers = JSON.parse(localStorage.getItem('lastLottoNumbers')) || null; // Store last recommended numbers

        function analyzeGlobalHistory() {
            if (globalWeights) return;
            globalWeights = {};
            for (let i = 1; i <= 45; i++) globalWeights[i] = 10; // Base weight

            const history = window.lottoHistory || {};
            const rounds = Object.keys(history).map(Number).sort((a, b) => b - a); // Newest first

            // Recency Weighting: Newer rounds have more influence
            rounds.forEach((r, idx) => {
                const nums = history[String(r)];
                if (!nums) return;

                // Weight decay: Recent 10 rounds get +5, others get +1
                const weightBoost = idx < 10 ? 5 : 1;

                // Only consider main numbers (first 6)
                for (let i = 0; i < 6; i++) {
                    if (nums[i]) globalWeights[nums[i]] += weightBoost;
                }
            });
            console.log("Global Analysis Complete:", globalWeights);
        }

        /**
         * 🔮 Advanced Lucky Number Generator
         * Uses Global Weights + Shop Pattern + Statistical Filters
         */
        function generateLuckyNumbers(storeWins, mode = 'mix') {
            // Ensure global analysis is done
            if (!globalWeights) analyzeGlobalHistory();

            // 1. Clone Global Weights for this session
            const currentWeights = { ...globalWeights };

            // 2. Apply Shop-Specific Weights based on Mode
            // storeWins: [{r: 1000, m: '자동'}, ...]
            const history = window.lottoHistory || {};
            let matchCount = 0;

            storeWins.forEach(win => {
                const isAuto = win.m.includes('자동');
                const isManual = win.m.includes('수동');

                // Logic: 
                // If mode is 'auto', heavily boost numbers from 'auto' wins.
                // If mode is 'manual', heavily boost numbers from 'manual' wins.
                // If mode is 'mix', boost all.
                let process = false;
                if (mode === 'auto' && isAuto) process = true;
                else if (mode === 'manual' && isManual) process = true;
                else if (mode === 'mix') process = true;

                if (process) {
                    const nums = history[String(win.r)];
                    if (nums) {
                        nums.slice(0, 6).forEach(n => {
                            currentWeights[n] += 50; // Massive boost for shop's winning pattern
                        });
                        matchCount++;
                    }
                }
            });

            // Fallback: If no matches for mode (e.g., asking for Manual but shop only has Auto wins),
            // then analyze ALL wins of this shop to find at least some "Shop Energy".
            if (matchCount === 0 && storeWins.length > 0) {
                storeWins.forEach(win => {
                    const nums = history[String(win.r)];
                    if (nums) {
                        nums.slice(0, 6).forEach(n => {
                            currentWeights[n] += 20; // Moderate boost
                        });
                    }
                });
            }

            // 3. Statistical Filter Loop
            // Try to generate a valid set that meets strict statistical criteria
            let bestSet = null;
            let maxAttempts = 200; // Hard limit

            for (let i = 0; i < maxAttempts; i++) {
                const candidate = drawSet(currentWeights);
                if (validateSet(candidate)) {
                    bestSet = candidate;
                    break;
                }
            }

            // If we failed to find a "perfect" set, just take the last raw one
            if (!bestSet) bestSet = drawSet(currentWeights);

            return {
                numbers: bestSet.sort((a, b) => a - b),
                historyCount: storeWins.length,
                relatedRounds: storeWins.map(w => w.r).slice(0, 5)
            };
        }

        function drawSet(weights) {
            const selected = new Set();
            // Safety copy to modify weights during draft (avoid picking same num)
            // But for simple Weighted Random without replacement, we just check 'has'

            while (selected.size < 6) {
                const n = weightedRandom(weights);
                selected.add(n);
            }
            return Array.from(selected);
        }

        function weightedRandom(weights) {
            let sum = 0;
            for (let i in weights) sum += weights[i];
            let rand = Math.random() * sum;
            for (let i in weights) {
                rand -= weights[i];
                if (rand < 0) return parseInt(i);
            }
            return Math.floor(Math.random() * 45) + 1;
        }

        // --- Probability Booster Filters ---
        function validateSet(numbers) {
            // Sort first
            numbers.sort((a, b) => a - b);

            // 1. Sum Filter: Winning sums usually fall between 100 ~ 175
            const sum = numbers.reduce((a, b) => a + b, 0);
            if (sum < 100 || sum > 175) return false;

            // 2. Odd/Even Ratio: Avoid 6:0 or 0:6. Accept 4:2, 3:3, 2:4
            const odds = numbers.filter(n => n % 2 !== 0).length;
            if (odds < 2 || odds > 4) return false;

            // 3. High/Low Ratio: (1-22) vs (23-45). Avoid 6:0 or 0:6
            const low = numbers.filter(n => n <= 22).length;
            if (low < 2 || low > 4) return false;

            // 4. Consecutive Check: Max 2 consecutive numbers allowed (e.g. 1,2,3 is bad)
            let consecutiveCnt = 0;
            for (let i = 0; i < numbers.length - 1; i++) {
                if (numbers[i] + 1 === numbers[i + 1]) {
                    consecutiveCnt++;
                    // If we have 2 pairs (1-2, 5-6) it's ok, but 1-2-3 (2 consecutives in a row) is rare
                    // Let's strictly disallow 3 consecutive numbers (1,2,3)
                    if (i > 0 && numbers[i - 1] + 1 === numbers[i]) return false;
                }
            }

            // 5. Last Digit Sum (Optimization): Usually ends in 0-9 spread 
            // (Optional, skip for performance)

            return true;
        }

        function applyFilters() {
            const minR = parseInt(document.getElementById('minRound').value) || 0;
            const maxR = parseInt(document.getElementById('maxRound').value) || 9999;
            const auto = document.getElementById('methodAuto').checked;
            const manual = document.getElementById('methodManual').checked;
            const semi = document.getElementById('methodSemi').checked;

            // Frequency Filters
            const f5 = document.getElementById('freq5').checked;
            const f3 = document.getElementById('freq3').checked;
            const f1 = document.getElementById('freq1').checked;
            const excludeClosed = document.getElementById('excludeClosed').checked;

            // ===== 1단계: 회차 + 당첨방식 + 폐업 여부 필터 =====
            const roundFiltered = allData.filter(d => {
                // 폐업점 제외 체크 시 폐업 데이터 숨김
                if (excludeClosed && d.closed) return false;

                const rMatch = d.r >= minR && d.r <= maxR;
                let mMatch = false;
                if (auto && d.m.includes('자동')) mMatch = true;
                if (manual && d.m.includes('수동')) mMatch = true;
                if (semi && d.m.includes('반자동')) mMatch = true;

                return rMatch && mMatch;
            });

            // ===== 2단계: 매장별 전체 당첨 횟수 계산 (회차 범위 필터와 상관없이 상점 인식) =====
            const shopWinsInRange = {};
            allData.forEach(item => {
                // roundFiltered 대신 allData를 사용하여 해당 상점의 역대 모든 당첨 횟수를 집계합니다.
                const key = (item.n || '').trim() + '|' + (item.a || '').trim();
                shopWinsInRange[key] = (shopWinsInRange[key] || 0) + 1;
            });

            // 필터링된 데이터(회차 범위 내)에 위에서 계산한 전체 당첨 횟수를 부여합니다.
            roundFiltered.forEach(item => {
                const key = (item.n || '').trim() + '|' + (item.a || '').trim();
                item.winsInRange = shopWinsInRange[key];
            });


            // ===== 3단계: Frequency 필터 적용 (선택 범위 내 횟수 기준) =====
            const filtered = roundFiltered.filter(d => {
                let fMatch = false;
                if (f5 && d.winsInRange >= 5) fMatch = true;
                if (f3 && d.winsInRange >= 3 && d.winsInRange <= 4) fMatch = true;
                if (f1 && d.winsInRange <= 2) fMatch = true;

                return fMatch;
            });

            document.getElementById('filteredCount').innerText = filtered.length.toLocaleString();
            updateMarkers(filtered);
            // updateRecentRounds(maxR); // Removed as per user request
        }

        function refreshRecentRounds(skipNotice = false) {
            const maxR = parseInt(document.getElementById('maxRound').value) || 9999;
            updateRecentRounds(maxR);

            // 261회 이하인 경우 추가 안내 토스트 (skipNotice가 false일 때만)
            if (!skipNotice && maxR <= 261) {
                showToast(`1등점 지도제공은<br><strong style="color:red;">262회차</strong>부터<br>제공됩니다`, "info", false, 'filter-notice-toast');
            }
        }

        // Toggle dropdown menu
        function toggleRecentDropdown() {
            const menu = document.getElementById('recentDropdownMenu');
            menu.classList.toggle('show');
        }

        // Close dropdown when clicking outside
        document.addEventListener('click', function (event) {
            const dropdown = document.querySelector('.recent-dropdown');
            const menu = document.getElementById('recentDropdownMenu');
            if (dropdown && !dropdown.contains(event.target) && menu) {
                menu.classList.remove('show');
            }
        });

        function setRecentNRounds(n) {
            let currentMax = parseInt(document.getElementById('maxRound').value);
            // 입력값이 없거나 유효하지 않으면 기본 최신 회차(1211) 사용
            if (isNaN(currentMax) || currentMax < 1) {
                currentMax = 1211;
            }

            // "전체" 옵션 처리
            if (n === 'all') {
                document.getElementById('maxRound').value = currentMax;
                document.getElementById('minRound').value = 1;

                // 드롭다운 버튼 텍스트 업데이트
                const toggleBtn = document.querySelector('.dropdown-toggle');
                if (toggleBtn) {
                    toggleBtn.childNodes[0].textContent = '전체';
                }
            } else {
                // 숫자인 경우 (10, 20, 30, 50, 100)
                document.getElementById('maxRound').value = currentMax;
                document.getElementById('minRound').value = Math.max(1, currentMax - (n - 1));

                // 드롭다운 버튼 텍스트 업데이트
                const toggleBtn = document.querySelector('.dropdown-toggle');
                if (toggleBtn) {
                    toggleBtn.childNodes[0].textContent = `최근 ${n}회`;
                }
            }

            // 드롭다운 닫기
            const menu = document.getElementById('recentDropdownMenu');
            if (menu) {
                menu.classList.remove('show');
            }

            // 지도 마커 및 하단 당첨번호 대시보드 즉시 갱신
            applyFilters();
            refreshRecentRounds(true); // 알림 중복 방지를 위해 skipNotice=true 전달

            if (currentMax <= 261) {
                showToast(`1등점 지도제공은<br><strong style="color:red;">262회차</strong>부터<br>제공됩니다`, "info", false, 'filter-notice-toast');
            } else {
                const displayText = n === 'all' ? '전체' : `최근${n}회차`;
                showToast(`${currentMax}회 기준 ${displayText} 데이터로 갱신되었습니다.`, "success", false, 'filter-notice-toast');
            }
        }

        // 기존 setRecent10Rounds 함수 유지 (하위 호환성)
        function setRecent10Rounds() {
            setRecentNRounds(10);
        }

        function updateRecentRounds(maxRound) {
            const container = document.getElementById('recentRoundsList');
            const refSpan = document.getElementById('recentRefRound');
            if (refSpan) refSpan.innerText = maxRound;

            if (!container) return;

            container.innerHTML = '';

            // Check if history data is loaded
            if (!window.lottoHistory) {
                container.innerHTML = '<div style="font-size:12px; color:#666; text-align:center;">데이터 로딩 중...</div>';
                return;
            }

            // Loop 3 rounds: maxRound, maxRound-1, maxRound-2 (Reduced to save space)
            for (let i = 0; i < 3; i++) {
                const targetRound = maxRound - i;
                if (targetRound < 1) continue; // No rounds below 1

                const row = document.createElement('div');
                row.className = 'recent-row';

                // Apply Highlight to the absolute newest round (1211)
                if (targetRound === 1211) {
                    row.classList.add('latest-round-glow');
                }

                // Round Number
                const roundNum = document.createElement('span');
                roundNum.className = 'recent-round-num';
                roundNum.innerText = targetRound + '회';
                row.appendChild(roundNum);

                // Balls Container
                const ballsDiv = document.createElement('div');
                ballsDiv.style.display = 'flex';
                ballsDiv.style.alignItems = 'center'; // Vertically center items
                ballsDiv.style.gap = '2px';

                // Get Winning Numbers
                // lottoHistory key is string "1210"
                const nums = window.lottoHistory[String(targetRound)];

                if (nums && nums.length > 0) {
                    // Separate Main (6) and Bonus (1)
                    // The 7th number is the bonus number in our JSON structure
                    const mainNums = nums.slice(0, 6).sort((a, b) => a - b);
                    const bonusNum = nums[6];

                    // Render Main Numbers
                    mainNums.forEach(n => {
                        const ball = document.createElement('span');
                        ball.className = 'mini-ball ' + getBallColor(n);
                        ball.innerText = n;
                        ballsDiv.appendChild(ball);
                    });

                    // Render Plus Sign
                    const plusSpan = document.createElement('span');
                    plusSpan.innerText = '+';
                    plusSpan.style.color = '#999';
                    plusSpan.style.fontSize = '12px';
                    plusSpan.style.fontWeight = 'bold';
                    plusSpan.style.margin = '0 2px';
                    ballsDiv.appendChild(plusSpan);

                    // Render Bonus Number
                    const bonusBall = document.createElement('span');
                    bonusBall.className = 'mini-ball ' + getBallColor(bonusNum);
                    bonusBall.innerText = bonusNum;
                    ballsDiv.appendChild(bonusBall);

                } else {
                    const noData = document.createElement('span');
                    noData.style.fontSize = '11px';
                    noData.style.color = '#999';
                    noData.innerText = '데이터 없음';
                    ballsDiv.appendChild(noData);
                }

                row.appendChild(ballsDiv);
                container.appendChild(row);
            }
        }

        function updateMarkers(data) {
            clusterer.clear();
            markers.forEach(m => m.setMap(null));
            markers = [];

            // To avoid duplicate markers for the same shop at the same location,
            // we need to group the filtered data by shop (lat, lng, name, address)
            // and then create a single marker for each unique shop.
            const uniqueShops = {};
            data.forEach(d => {
                const key = `${d.lat}_${d.lng}_${d.n}_${d.a}`;
                if (!uniqueShops[key]) {
                    uniqueShops[key] = {
                        n: d.n,
                        a: d.a,
                        lat: d.lat,
                        lng: d.lng,
                        totalWins: d.totalWins, // This is the total wins for the shop
                        closed: d.closed, // Store closed status
                        rounds: [] // To store individual round details for infowindow
                    };
                }
                uniqueShops[key].rounds.push({ r: d.r, m: d.m });
            });

            Object.values(uniqueShops).forEach(shop => {
                let markerImg = null;
                // Tiered Styles
                if (shop.totalWins >= 5) {
                    // Legendary Gold Star
                    markerImg = new kakao.maps.MarkerImage(
                        'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png',
                        new kakao.maps.Size(24, 35)
                    );
                } else if (shop.totalWins >= 3) {
                    // Professional Red
                    markerImg = new kakao.maps.MarkerImage(
                        'https://t1.daumcdn.net/localimg/localimages/07/2018/pc/img/marker_spot.png',
                        new kakao.maps.Size(24, 35),
                        { offset: new kakao.maps.Point(12, 35) }
                    );
                }

                // Closed Shop Override
                if (shop.closed) {
                    markerImg = new kakao.maps.MarkerImage(
                        'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_red.png',
                        new kakao.maps.Size(31, 35)
                    );
                }

                const marker = new kakao.maps.Marker({
                    position: new kakao.maps.LatLng(shop.lat, shop.lng),
                    image: markerImg
                });
                marker.shopData = shop; // Store shop data for retrieval

                const sortedRounds = shop.rounds.sort((a, b) => b.r - a.r);
                let roundTagsHtml = sortedRounds.map(r => `<span class="iw-tag">${r.r}회(${r.m})</span>`).join('');

                if (shop.closed) {
                    roundTagsHtml = `<span class="iw-tag" style="background:#ff5252; color:white; font-weight:bold;">⛔ 폐업/휴업</span>` + roundTagsHtml;
                }

                // Helper to format address for mobile: break after the street number
                const formatAddrForMobile = (addr) => {
                    if (!addr) return "";
                    // Regex: Find the first sequence of digits followed by a space and insert mobile-only BR
                    return addr.replace(/(\d+)\s/, '$1<br class="mobile-br"> ');
                };
                const displayAddr = formatAddrForMobile(shop.a);

                const safeAddr = (shop.a || "").replace(/'/g, "\\'").replace(/\n/g, " ");
                const safeName = (shop.n || "").replace(/'/g, "\\'").replace(/\n/g, " ");

                const content = `
                    <div class="infowindow">
                        <div class="iw-title">${shop.n} ${shop.totalWins >= 5 ? '🌟' : ''} ${shop.closed ? '<span style="font-size:12px; color:red;">(폐업)</span>' : ''}</div>
                        <div class="iw-addr-box" onclick="openRoadviewWithCopy(${shop.lat}, ${shop.lng}, '${safeName}', '${safeAddr}')" title="주소 복사 (로드뷰 보기)">
                            <span class="iw-addr">${displayAddr}</span>
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="#666"><path d="M16 1H4c-1.11 0-2 .9-2        3h12         c-1.1 0-2 .9-2 2v14c0 1.1.9 2          1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
                                                       <div style="font-weight:bold; color:red; margin-bottom:5px;">총 ${shop.totalWins}회 당첨</div>
                        <div class="iw-details">${roundTagsHtml}</div>
                        <button class="btn-gold" onclick="openAdModal('${safeName}', '${safeAddr}', ${shop.lat}, ${shop.lng}, ${shop.totalWins}, ${shop.closed})">
                            ✨ 이번 주 1등 추천 번호 받기
                        </button>
                        <div class="iw-actions">
                            <button class="btn-iw btn-navi" onclick="openRoadviewWithNavi(${shop.lat}, ${shop.lng}, '${safeName}', '${safeAddr}')">
                                로드뷰(ROAD VIEW) 보기
                            </button>
                        </div>
                    </div>
                `;

                const infowindow = new kakao.maps.InfoWindow({
                    content: content,
                    removable: true,
                    zIndex: 10000 // Ensure popup is on top of everything (User Request)
                });

                kakao.maps.event.addListener(marker, 'click', () => {
                    // Force close ALL toasts immediately
                    closeAllToasts();

                    // Close previous InfoWindow if exists
                    if (currentInfoWindow) {
                        currentInfoWindow.close();
                        document.body.classList.remove('iw-open');
                    }

                    // Mobile Focus Mode: Hide distractions
                    if (window.innerWidth <= 768) {
                        document.body.classList.add('iw-open');
                    }

                    infowindow.open(map, marker);
                    currentInfoWindow = infowindow; // Update current
                });

                // Listen for native close event (e.g. X button)
                kakao.maps.event.addListener(infowindow, 'close', function () {
                    document.body.classList.remove('iw-open');
                });

                markers.push(marker);
            });
            clusterer.addMarkers(markers);
        }

        /**
         * GPS Location Service Module
         * Handles user positioning, nearest shop calculation, and UI feedback (Toasts).
         */
        let myLocationMarker = null;

        function requestMyLocation() {
            if (!navigator.onLine) {
                showToast("🌐 인터넷 연결이 끊겨 있습니다. 네트워크를 확인해 주세요.", "error");
                return;
            }

            if (!navigator.geolocation) {
                showToast("🚫 이 브라우저에서는 위치 정보를 사용할 수 없습니다.", "error");
                return;
            }

            const gpsBtn = document.querySelector('.gps-button');
            if (gpsBtn) gpsBtn.classList.add('loading');

            // GPS Permission & Fetch
            navigator.geolocation.getCurrentPosition(
                (pos) => {
                    if (gpsBtn) gpsBtn.classList.remove('loading');
                    const lat = pos.coords.latitude;
                    const lng = pos.coords.longitude;
                    const center = new kakao.maps.LatLng(lat, lng);

                    map.setCenter(center);

                    // Close all infowindows to clear the view
                    if (typeof clusterer !== 'undefined') {
                        // There's no direct 'closeAll' on clusterer, but we can just let it be
                    }

                    // Add/Update Blue Dot Marker
                    if (!myLocationMarker) {
                        myLocationMarker = new kakao.maps.CustomOverlay({
                            position: center,
                            content: `
                                <div style="position:relative;">
                                    <div class="pulse"></div>
                                    <div style="width:16px; height:16px; background:#1976d2; border:2px solid #fff; border-radius:50%; box-shadow:0 0 10px rgba(0,0,0,0.5); position:relative; z-index:2; transform: translate(-50%, -50%);"></div>
                                </div>
                            `,
                            map: map,
                            zIndex: 1001
                        });
                    } else {
                        myLocationMarker.setPosition(center);
                        myLocationMarker.setMap(map);
                    }

                    findNearestShop(lat, lng);
                },
                (err) => {
                    console.error("GPS Error:", err);
                    if (gpsBtn) gpsBtn.classList.remove('loading');
                    let msg = "위치 정보를 가져오는 데 실패했습니다.";
                    switch (err.code) {
                        case 1:
                            msg = "위치 정보 권한이 거부되었습니다. 브라우저 설정에서 위치 권한을 허용해 주세요.";
                            break;
                        case 2:
                            msg = "위치 정보를 사용할 수 없습니다. GPS가 켜져 있는지 확인해 주세요.";
                            break;
                        case 3:
                            msg = "위치 정보를 가져오는 데 시간이 초과되었습니다. 다시 시도해 보세요.";
                            break;
                    }
                    showToast(msg, "error");
                },
                // 정확도를 true로 변경하고 타임아웃을 조정하여 응답성을 높입니다.
                { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
            );
        }



        // --- Monetization & Logic ---
        let currentShopData = null; // Store temp data for the modal

        function openAdModal(name, addr, lat, lng, totalWins, isClosed) {
            // 폐업 점포 체크 (260210)
            if (isClosed) {
                alert("현재 폐업점으로 추천번호 제공이 불가능한 점포입니다");
                return;
            }

            // Re-filter allData for this specific shop to get rounds.
            const rounds = allData.filter(d => d.n === name && d.a === addr).map(d => ({ r: d.r, m: d.m }));

            currentShopData = { name, addr, lat, lng, totalWins, rounds };

            // Show Modal
            const modal = document.getElementById('adModal');
            const adContent = document.getElementById('adContent');
            const resultContent = document.getElementById('resultContent');

            // Mode Containers
            const modeSelection = document.getElementById('modeSelection');
            const analysisLoading = document.getElementById('analysisLoading');
            const modeDreamInput = document.getElementById('modeDreamInput');
            const modeHoroscopeSelect = document.getElementById('modeHoroscopeSelect');

            modal.style.display = 'flex';
            adContent.style.display = 'flex'; // Changed to flex for centering
            resultContent.style.display = 'none';

            // Reset UI State (CRITICAL: Reset result text structure)
            const resultInfo = document.getElementById('resultInfoText');
            if (resultInfo) {
                resultInfo.innerHTML = `이 명당은 과거 <strong id="paramHCount" style="color:#fae100;">0</strong>번의 1등을 배출했습니다.<br>
                    (<span id="paramRounds"></span> 등)`;
            }

            modeSelection.style.display = 'block';
            if (analysisLoading) analysisLoading.style.display = 'none';
            if (modeDreamInput) modeDreamInput.style.display = 'none';
            if (modeHoroscopeSelect) modeHoroscopeSelect.style.display = 'none';

            // Push history state to support Back Button closing
            history.pushState({ modalOpen: true }, null, "");
        }

        // --- Phase 10: Selection Handlers ---

        function selectAnalysisMode() {
            // Hide selection, show loading
            document.getElementById('modeSelection').style.display = 'none';
            const loader = document.getElementById('analysisLoading');
            if (loader) {
                loader.style.display = 'flex';
                // Reset text if needed
                loader.querySelector('h3').innerText = '데이터 분석 중...';
                loader.querySelector('p').innerText = '명당의 기운을 모으고 있습니다';
            }

            // Simulate Analysis Delay (3 seconds)
            setTimeout(() => {
                showResult();
            }, 3000);
        }

        function selectDreamMode() {
            document.getElementById('modeSelection').style.display = 'none';
            document.getElementById('modeDreamInput').style.display = 'block';
        }

        function resetToModeSelection() {
            document.getElementById('modeDreamInput').style.display = 'none';
            document.getElementById('modeHoroscopeSelect').style.display = 'none';
            document.getElementById('modeSelection').style.display = 'block';
        }

        function handleDreamTag(keyword) {
            document.getElementById('dreamInput').value = keyword;
            handleDreamSubmit();
        }

        function handleDreamSubmit() {
            const input = document.getElementById('dreamInput');
            const keyword = input.value.trim();

            if (!keyword) {
                alert('꿈 내용을 입력해주세요!');
                return;
            }

            // Show loading state
            document.getElementById('modeDreamInput').style.display = 'none';
            const loader = document.getElementById('analysisLoading');
            if (loader) {
                loader.style.display = 'flex';
                loader.querySelector('h3').innerText = '꿈 해몽 중...';
                loader.querySelector('p').innerText = '꿈 속에 숨겨진 행운을 찾고 있습니다';
            }

            setTimeout(() => {
                const luckyNumbers = generateDreamNumbers(keyword);
                showResult(luckyNumbers);
            }, 2000);
        }

        function generateDreamNumbers(keyword) {
            // 1. Traditional Dream Mappings (Simple Version)
            const dreamMap = {
                '돼지': [8, 12, 23, 33, 38, 41],
                '똥': [6, 17, 24, 35, 36, 42],
                '조상': [1, 3, 15, 27, 39, 41],
                '불': [2, 11, 22, 33, 40, 44],
                '물': [4, 9, 21, 26, 31, 37],
                '뱀': [5, 10, 16, 28, 34, 45],
                '용': [7, 18, 20, 30, 42, 45]
            };

            // If keyword exists in map, return it (with small variation if needed, but fixed for now)
            if (dreamMap[keyword]) {
                return {
                    numbers: dreamMap[keyword],
                    historyCount: 0, // Not based on history
                    type: 'dream',
                    keyword: keyword
                };
            }

            // 2. Hash-based Generation for unknown keywords
            // This ensures the same keyword always yields the same numbers
            let hash = 0;
            for (let i = 0; i < keyword.length; i++) {
                hash = ((hash << 5) - hash) + keyword.charCodeAt(i);
                hash |= 0; // Convert to 32bit integer
            }

            // Seeding logic using text hash
            const seededRandom = (seed) => {
                var x = Math.sin(seed++) * 10000;
                return x - Math.floor(x);
            };

            const selected = new Set();
            let seed = Math.abs(hash);

            while (selected.size < 6) {
                const n = Math.floor(seededRandom(seed) * 45) + 1;
                selected.add(n);
                seed++;
            }

            return {
                numbers: Array.from(selected).sort((a, b) => a - b),
                historyCount: 0,
                type: 'dream',
                keyword: keyword
            };
        }

        function selectHoroscopeMode() {
            document.getElementById('modeSelection').style.display = 'none';
            document.getElementById('modeHoroscopeSelect').style.display = 'block';
        }

        function handleZodiacClick(zodiacName, icon) {
            // Show loading
            document.getElementById('modeHoroscopeSelect').style.display = 'none';
            const loader = document.getElementById('analysisLoading');
            if (loader) {
                loader.style.display = 'flex';
                loader.querySelector('h3').innerText = '오늘의 운세 분석 중...';
                loader.querySelector('p').innerText = '별들의 기운을 읽고 있습니다';
            }

            // Simulate and Generate
            setTimeout(() => {
                const horoscopeData = generateHoroscope(zodiacName);
                showResult({
                    type: 'horoscope',
                    zodiac: zodiacName,
                    icon: icon,
                    ...horoscopeData
                });
            }, 2000);
        }

        function generateHoroscope(zodiacName) {
            // Get today's date in Korea Standard Time (UTC+9)
            const now = new Date();
            const utc = now.getTime() + (now.getTimezoneOffset() * 60000);
            const koreaTime = new Date(utc + (9 * 60 * 60 * 1000));

            const year = koreaTime.getFullYear();
            const month = String(koreaTime.getMonth() + 1).padStart(2, '0');
            const day = String(koreaTime.getDate()).padStart(2, '0');
            const today = `${year}-${month}-${day}`;

            const key = today + zodiacName;

            // Generate seeded random based on date + zodiac
            let hash = 0;
            for (let i = 0; i < key.length; i++) {
                hash = ((hash << 5) - hash) + key.charCodeAt(i);
                hash |= 0;
            }
            const seededRandom = (seed) => {
                var x = Math.sin(seed++) * 10000;
                return x - Math.floor(x);
            };
            let seed = Math.abs(hash);

            // 1. Horoscope Text Pools
            const genFortunes = [
                "금기(金氣)의 영향으로 신중함이 요구되는 하루입니다.",
                "오늘은 당신의 날입니다. 무엇을 해도 술술 풀릴 것입니다.",
                "직감이 매우 뛰어난 날입니다. 당신의 느낌을 믿어보세요.",
                "귀인의 도움을 받아 어려움이 해결될 것입니다. 긍정적인 마음을 가지세요.",
                "행운의 여신이 당신을 보고 미소 짓고 있습니다.",
                "뜻밖의 행운이 찾아올 수 있습니다. 주변을 잘 살펴보세요.",
                "차분하게 내실을 다지면 더 큰 기회가 찾아올 것입니다.",
                "새로운 변화를 시도하기에 아주 적절한 시기입니다."
            ];

            const loveFortunes = [
                "말의 표현을 조절하세요. 배려가 필요한 시기입니다.",
                "소중한 사람과 즐거운 시간을 보내기에 좋은 날입니다.",
                "솔직한 감정 표현이 상대방의 마음을 움직일 것입니다.",
                "작은 오해가 생길 수 있으니 충분한 대화를 나누세요.",
                "새로운 인연이 나타날 수 있는 기운이 강합니다.",
                "서로에 대한 신뢰가 깊어지는 따뜻한 하루가 될 것입니다.",
                "당신의 매력이 돋보이는 날입니다. 자신감을 가지세요.",
                "가까운 사람과의 갈등은 먼저 손을 내미는 것이 좋습니다."
            ];

            const moneyFortunes = [
                "예상치 못한 지출에 대비하세요. 신중한 소비가 필요합니다.",
                "금전운이 매우 좋습니다. 작은 투자도 결실을 맺을 수 있습니다.",
                "재물운이 상승하는 시기입니다. 로또 구매하기 딱 좋은 날!",
                "지갑 관리에 신경 써야 하는 하루입니다. 충동구매를 주의하세요.",
                "생각지 못한 곳에서 작은 수익이 발생할 수 있습니다.",
                "계획적인 소비가 당신에게 더 큰 행운을 불러올 것입니다.",
                "금전적인 이득보다는 인맥을 쌓는 것이 장기적으로 유리합니다.",
                "뿌린 대로 거두는 날입니다. 성실함이 보상으로 돌아옵니다."
            ];

            const luckyColors = ["빨강", "파랑", "노랑", "초록", "보라", "금색", "은색", "흰색", "검정", "주황"];

            const genIdx = Math.floor(seededRandom(seed) * genFortunes.length);
            const loveIdx = Math.floor(seededRandom(seed + 1) * loveFortunes.length);
            const moneyIdx = Math.floor(seededRandom(seed + 2) * moneyFortunes.length);
            const colorIdx = Math.floor(seededRandom(seed + 3) * luckyColors.length);

            const text = `
                <div style="text-align:left; margin: 0 auto; max-width:280px; line-height:1.8; font-size:14px;">
                    • <b>종합운</b> : ${genFortunes[genIdx]}<br>
                    • <b>애정운</b> : ${loveFortunes[loveIdx]}<br>
                    • <b>금전운</b> : ${moneyFortunes[moneyIdx]}<br>
                    • <b>행운의 색상</b> : ${luckyColors[colorIdx]}
                </div>
            `;

            // 2. Number Generation
            const selected = new Set();
            let numSeed = seed + 100;
            while (selected.size < 6) {
                const n = Math.floor(seededRandom(numSeed) * 45) + 1;
                selected.add(n);
                numSeed++;
            }

            return {
                text: text,
                numbers: Array.from(selected).sort((a, b) => a - b),
                historyCount: 0
            };
        }

        function closeModal() {
            // If the modal is open, going back will trigger popstate which closes it effectively
            // But we need to check if we are actually in the modal state
            if (document.getElementById('adModal').style.display === 'flex') {
                history.back();
            }
        }

        function _internalCloseModal() {
            document.getElementById('adModal').style.display = 'none';
        }

        function showResult(customResult = null) {
            document.getElementById('adContent').style.display = 'none';
            document.getElementById('resultContent').style.display = 'block';

            // Legal Disclaimer
            const legalDiv = document.getElementById('legalDisclaimer');
            if (!legalDiv) {
                const legal = document.createElement('div');
                legal.id = 'legalDisclaimer';
                legal.style.cssText = "font-size: 11px; color: rgba(255,255,255,0.5); margin-top: 15px; text-align: center; line-height: 1.4;";
                legal.innerHTML = "※ 본 서비스는 동행복권의 당첨 데이터를 기반으로 통계적/임의적 분석을 제공하며, 당첨을 보장하지 않습니다.<br>과도한 복권 구매는 도박 중독을 유발할 수 있습니다.";
                document.getElementById('resultContent').appendChild(legal);
            }

            const ballContainer = document.getElementById('luckyBalls');
            ballContainer.innerHTML = '';

            // Reset container styles
            ballContainer.style.flexDirection = 'column';
            ballContainer.style.gap = '5px';
            console.log("Layout Updated: Gap 5px");

            if (customResult) {
                // --- Dream / Horoscope Mode (Single Row) ---
                if (customResult.type === 'dream') {
                    const container = document.getElementById('resultInfoText');
                    if (container) {
                        container.innerHTML =
                            `꿈 키워드 <strong style="color:#fae100;">'${customResult.keyword}'</strong>(으)로<br>분석된 행운의 번호입니다.`;
                    }
                } else if (customResult.type === 'horoscope') {
                    const container = document.getElementById('resultInfoText');
                    if (container) {
                        container.innerHTML =
                            `<div class="horoscope-text-box">
                                <div style="font-size:24px; margin-bottom:5px;">${customResult.icon}</div>
                                <div style="font-weight:bold; font-size:16px; margin-bottom:10px; color:#fae100;">${customResult.zodiac}띠 오늘의 운세</div>
                                ${customResult.text}
                            </div>
                            <div style="font-size:13px; color:rgba(255,255,255,0.8);">위 운세에 기반한 행운의 번호입니다.</div>`;
                    }
                }


                // Render with Copy/OMR buttons using createRow helper
                const createRowForCustom = (numbers) => {
                    const mainContainer = document.createElement('div');
                    mainContainer.style.display = 'flex';
                    mainContainer.style.flexDirection = 'column';
                    mainContainer.style.alignItems = 'center';
                    mainContainer.style.width = '100%';

                    const rowWrapper = document.createElement('div');
                    rowWrapper.style.display = 'flex';
                    rowWrapper.style.alignItems = 'center';
                    rowWrapper.style.justifyContent = 'center';
                    rowWrapper.style.gap = '12px'; // Increased to ~0.3cm
                    rowWrapper.style.width = '100%';

                    // Balls
                    const ballsRow = document.createElement('div');
                    ballsRow.style.display = 'flex';
                    ballsRow.style.justifyContent = 'center';
                    ballsRow.style.gap = '5px';
                    ballsRow.style.flex = 'none';

                    numbers.forEach(n => {
                        const ball = document.createElement('div');
                        ball.className = 'ball ' + getBallColor(n);
                        ball.innerText = n;
                        ballsRow.appendChild(ball);
                    });
                    rowWrapper.appendChild(ballsRow);

                    // Buttons Column
                    const buttonsCol = document.createElement('div');
                    buttonsCol.style.display = 'flex';
                    buttonsCol.style.flexDirection = 'column';
                    buttonsCol.style.gap = '5px';
                    buttonsCol.style.minWidth = '90px';

                    // Copy Button
                    const copyBtn = document.createElement('div');
                    copyBtn.className = 'omr-action-btn';
                    copyBtn.innerHTML = '📋 복사';
                    copyBtn.style.justifyContent = 'center';
                    copyBtn.onclick = (e) => {
                        e.stopPropagation();
                        copyToClipboard(numbers);
                    };
                    buttonsCol.appendChild(copyBtn);

                    // OMR Button
                    const omrBtn = document.createElement('div');
                    omrBtn.className = 'omr-action-btn';
                    omrBtn.innerHTML = '📝 OMR 보기';
                    omrBtn.style.justifyContent = 'center';
                    omrBtn.onclick = (e) => {
                        e.stopPropagation();
                        openOMR(numbers);
                    };
                    buttonsCol.appendChild(omrBtn);

                    rowWrapper.appendChild(buttonsCol);
                    mainContainer.appendChild(rowWrapper);
                    return mainContainer;
                };

                ballContainer.appendChild(createRowForCustom(customResult.numbers));

                // Store last recommended numbers for quick OMR access
                lastRecommendedNumbers = customResult.numbers;
                localStorage.setItem('lastLottoNumbers', JSON.stringify(lastRecommendedNumbers));

            } else {
                // --- Standard Analysis Mode (Auto + Manual) ---
                // Generate two sets with specific modes
                const resultAuto = generateLuckyNumbers(currentShopData.rounds, 'auto');
                const resultManual = generateLuckyNumbers(currentShopData.rounds, 'manual');

                // Update Info Text (Shared stats)
                const container = document.getElementById('resultInfoText');
                if (container) {
                    container.innerHTML =
                        `이 명당은 과거 <strong id="paramHCount" style="color:#fae100;">${resultAuto.historyCount}</strong>번의 1등을 배출했습니다.<br>` +
                        `(<span id="paramRounds">${resultAuto.relatedRounds.join(', ') + (resultAuto.historyCount > 5 ? '...' : '')}</span> 등)`;
                }

                // Helper to create a unified row component
                const createRow = (label, numbers, isManual = false) => {
                    // Main Container (Vertical stack for Row + Optional Link)
                    const mainContainer = document.createElement('div');
                    mainContainer.style.display = 'flex';
                    mainContainer.style.flexDirection = 'column';
                    mainContainer.style.alignItems = 'center';
                    mainContainer.style.width = '100%';
                    mainContainer.style.marginBottom = '2px';

                    // Row (Label + Balls + Buttons)
                    const rowWrapper = document.createElement('div');
                    rowWrapper.style.display = 'flex';
                    rowWrapper.style.alignItems = 'center';
                    rowWrapper.style.justifyContent = 'center';
                    rowWrapper.style.gap = '12px'; // Increased to ~0.3cm
                    console.log("Horizontal Layout Updated: Gap 12px");
                    rowWrapper.style.width = '100%';
                    rowWrapper.className = 'result-row-wrapper'; // Add class for mobile layout

                    // Label
                    const labelDiv = document.createElement('div');
                    labelDiv.className = 'result-label'; // Add class for mobile layout
                    labelDiv.innerHTML = `<span style="color:#fae100; font-weight:bold; font-size:16px;">[${label}]</span>`;
                    // labelDiv.style.minWidth = '50px'; // Removed min-width to reduce gap
                    rowWrapper.appendChild(labelDiv);

                    // Balls
                    const ballsRow = document.createElement('div');
                    ballsRow.className = 'result-balls'; // Add class for mobile layout
                    ballsRow.style.display = 'flex';
                    ballsRow.style.justifyContent = 'center';
                    ballsRow.style.gap = '5px';
                    ballsRow.style.flex = 'none';

                    numbers.forEach(n => {
                        const ball = document.createElement('div');
                        ball.className = 'ball ' + getBallColor(n);
                        ball.innerText = n;
                        ballsRow.appendChild(ball);
                    });
                    rowWrapper.appendChild(ballsRow);

                    // Buttons Column (Copy / OMR stacked vertically)
                    const buttonsCol = document.createElement('div');
                    buttonsCol.style.display = 'flex';
                    buttonsCol.style.flexDirection = 'column';
                    buttonsCol.style.gap = '5px';
                    buttonsCol.style.minWidth = '90px';

                    // Copy Button
                    const copyBtn = document.createElement('div');
                    copyBtn.className = 'omr-action-btn';
                    copyBtn.innerHTML = '📋 복사';
                    copyBtn.style.justifyContent = 'center';
                    copyBtn.onclick = (e) => {
                        e.stopPropagation();
                        copyToClipboard(numbers);
                    };
                    buttonsCol.appendChild(copyBtn);

                    // OMR Button
                    const omrBtn = document.createElement('div');
                    omrBtn.className = 'omr-action-btn';
                    omrBtn.innerHTML = '📝 OMR 보기';
                    omrBtn.style.justifyContent = 'center';
                    omrBtn.onclick = (e) => {
                        e.stopPropagation();
                        openOMR(numbers);
                    };
                    buttonsCol.appendChild(omrBtn);

                    rowWrapper.appendChild(buttonsCol);
                    mainContainer.appendChild(rowWrapper);

                    // Link for Manual
                    if (isManual) {
                        const linkBtn = document.createElement('div');
                        linkBtn.innerHTML = '📊 번호별 출현 횟수 참고하기 >';
                        linkBtn.style.color = '#fae100';
                        linkBtn.style.fontSize = '12px';
                        linkBtn.style.marginTop = '5px';
                        linkBtn.style.cursor = 'pointer';
                        linkBtn.style.textDecoration = 'underline';
                        linkBtn.style.opacity = '1';
                        linkBtn.onclick = (e) => {
                            e.stopPropagation();
                            showStats();
                        };
                        mainContainer.appendChild(linkBtn);
                    }

                    return mainContainer;
                };

                ballContainer.appendChild(createRow('자동', resultAuto.numbers));
                ballContainer.appendChild(createRow('수동', resultManual.numbers, true));

                // Store last recommended numbers (Auto mode) for quick OMR access
                lastRecommendedNumbers = resultAuto.numbers;
                localStorage.setItem('lastLottoNumbers', JSON.stringify(lastRecommendedNumbers));
            }
        }

        function getBallColor(n) {
            if (n <= 10) return 'one';
            if (n <= 20) return 'two';
            if (n <= 30) return 'three';
            if (n <= 40) return 'four';
            return 'five';
        }

        function goToShop() {
            if (!currentShopData) return;
            openDirections(currentShopData.lat, currentShopData.lng, currentShopData.name);
            closeModal();
        }

        // --- Side Nav Controls ---
        function toggleNav() {
            const nav = document.getElementById('sideNav');
            const overlay = document.getElementById('sideNavOverlay');
            const btn = document.getElementById('menuBtn');
            const isOpen = nav.classList.contains('open');

            if (isOpen) {
                closeNav();
            } else {
                nav.classList.add('open');
                overlay.style.display = 'block';
                setTimeout(() => overlay.classList.add('show'), 10);
                btn.classList.add('active');
            }
        }

        function closeNav() {
            const nav = document.getElementById('sideNav');
            const overlay = document.getElementById('sideNavOverlay');
            const btn = document.getElementById('menuBtn');

            nav.classList.remove('open');
            overlay.classList.remove('show');
            setTimeout(() => {
                if (!nav.classList.contains('open')) {
                    overlay.style.display = 'none';
                }
            }, 300);
            btn.classList.remove('active');
        }

        let currentFreqPeriod = 0; // 0 for All, N for last N weeks

        function showStats() {
            closeNav();
            const modal = document.getElementById('statModal');
            modal.style.display = 'flex';
            currentFreqPeriod = 0; // Reset to All
            updateFreqFilterUI();
            renderFrequencyStats();
        }

        function closeStatModal() {
            document.getElementById('statModal').style.display = 'none';
        }

        function setFreqPeriod(period) {
            currentFreqPeriod = period;
            updateFreqFilterUI();
            renderFrequencyStats();
        }

        function updateFreqFilterUI() {
            const items = document.querySelectorAll('.freq-filter-item');
            items.forEach(item => {
                const onclickStr = item.getAttribute('onclick');
                const p = parseInt(onclickStr.match(/\d+/)[0]);
                if (p === currentFreqPeriod) {
                    item.classList.add('active');
                } else {
                    item.classList.remove('active');
                }
            });
        }

        function renderFrequencyStats() {
            const container = document.getElementById('freqListContainer');
            const rangeText = document.getElementById('freqRangeText');
            if (!window.lottoHistory) {
                container.innerHTML = '<div style="text-align:center; padding:20px; color:red;">데이터를 불러올 수 없습니다.</div>';
                return;
            }

            // Get sorted rounds
            const rounds = Object.keys(window.lottoHistory).map(Number).sort((a, b) => b - a);
            const totalRoundsAvailable = rounds.length;
            const maxR = rounds[0];

            let targetRounds = rounds;
            let minR = rounds[rounds.length - 1];

            if (currentFreqPeriod > 0) {
                targetRounds = rounds.slice(0, currentFreqPeriod);
                minR = targetRounds[targetRounds.length - 1];
            }

            rangeText.innerText = `${minR}회 ~ ${maxR}회`;

            // 1. Calculate frequencies for the selected range (1-45)
            const counts = {};
            for (let i = 1; i <= 45; i++) counts[i] = 0;

            targetRounds.forEach(r => {
                const nums = window.lottoHistory[r.toString()];
                nums.forEach(n => {
                    if (counts[n] !== undefined) counts[n]++;
                });
            });

            // 2. Convert to array and sort by frequency (descending)
            const sorted = Object.keys(counts).map(num => ({
                num: parseInt(num),
                count: counts[num]
            })).sort((a, b) => b.count - a.count || a.num - b.num);

            const maxCount = sorted.length > 0 ? sorted[0].count : 0;

            // 3. Render
            let html = '';
            sorted.forEach((item, index) => {
                const percentage = maxCount > 0 ? (item.count / maxCount) * 100 : 0;
                const paddedNum = item.num < 10 ? '0' + item.num : item.num;
                html += `
                    <div class="freq-row">
                        <div class="freq-ball">${paddedNum}</div>
                        <div class="freq-bar-container">
                            <div class="freq-bar-fill" style="width: ${percentage}%"></div>
                        </div>
                        <div class="freq-count">${item.count}</div>
                    </div>
                `;
            });

            container.innerHTML = html;
        }

        let html5QrCode = null;

        function showQRScanner() {
            closeNav();
            const modal = document.getElementById('qrModal');
            modal.style.display = 'flex';

            // Reset Result
            document.getElementById('qrResult').style.display = 'none';
            document.getElementById('qr-reader').style.display = 'block';

            if (!html5QrCode) {
                html5QrCode = new Html5Qrcode("qr-reader");
            }

            const config = { fps: 10, qrbox: { width: 250, height: 250 } };

            // Start Camera (Prefer Environment)
            html5QrCode.start({ facingMode: "environment" }, config, onScanSuccess)
                .catch(err => {
                    console.error("Error starting QR scanner", err);
                    alert("카메라를 실행할 수 없습니다. 권한을 확인해주세요.\n" + err);
                    // Return to hamburger menu on permission denial or error
                    closeQRScanner();
                });
        }

        function closeQRScanner() {
            const modal = document.getElementById('qrModal');
            modal.style.display = 'none';

            if (html5QrCode) {
                if (html5QrCode.isScanning) {
                    html5QrCode.stop().then(() => {
                        html5QrCode.clear();
                        html5QrCode = null;
                        // Return to hamburger menu
                        toggleNav();
                    }).catch(err => {
                        console.log("Failed to stop qr code scanner", err);
                        toggleNav();
                    });
                } else {
                    html5QrCode.clear();
                    html5QrCode = null;
                    toggleNav();
                }
            } else {
                toggleNav();
            }
        }

        function restartQRScanner() {
            // Simply call showQRScanner to reuse the initialization logic
            // But we need to ensure previous instance is cleaned up if it exists in weird state?
            // Usually onScanSuccess cleans it up.
            showQRScanner();
        }

        function onScanSuccess(decodedText, decodedResult) {
            console.log(`Scan result: ${decodedText}`);
            if (decodedText.includes('dhlottery.co.kr') && decodedText.includes('v=')) {
                // Stop scanning
                if (html5QrCode) {
                    html5QrCode.stop().then(() => {
                        html5QrCode.clear();
                        html5QrCode = null; // Destroy instance to force fresh start next time
                        document.getElementById('qr-reader').style.display = 'none';
                        verifyLotteryQR(decodedText);
                    }).catch(err => console.error(err));
                }
            } else {
                // Continuous scanning...
            }
        }

        function verifyLotteryQR(url) {
            try {
                const urlObj = new URL(url);
                const v = urlObj.searchParams.get('v');
                if (!v) throw new Error("QR 데이터 파싱 실패 (v param missing)");

                // Format: ROUND + 'm' + NUMBERS...
                const parts = v.split('m');
                const round = parseInt(parts[0]);
                const rawNumbers = parts[1];

                document.getElementById('qrRound').innerText = round;

                // Get winning numbers
                const winNums = window.lottoHistory ? window.lottoHistory[String(round)] : null;
                const resultArea = document.getElementById('qrResult');
                resultArea.style.display = 'block';

                const listContainer = document.getElementById('qrGameList');
                listContainer.innerHTML = '';

                if (!winNums) {
                    listContainer.innerHTML = `<div style="padding:20px; text-align:center;">
                        ${round}회차 추첨 결과가 아직 없습니다.<br>
                        (토요일 오후 8시 35분 이후 확인 가능)
                    </div>`;
                    return;
                }

                // winNums: [n1, n2, n3, n4, n5, n6, bonus]
                const mainNums = winNums.slice(0, 6);
                const bonusNum = winNums[6];

                // Parse games
                const games = [];
                // rawNumbers string contains concatenated games.
                // It 'usually' splits by 'n' or other delimiters in older formats?
                // But the snippet saw `v.split('m')` logic.
                // Let's rely on fixed width 12 chars per game logic if possible, 
                // but safeguard against delimiters.
                // Removing non-digit characters is safer.
                const cleanNums = rawNumbers.replace(/[^0-9]/g, '');

                for (let i = 0; i < cleanNums.length; i += 12) {
                    const gameStr = cleanNums.substring(i, i + 12);
                    if (gameStr.length < 12) break;

                    const nums = [];
                    for (let j = 0; j < 12; j += 2) {
                        nums.push(parseInt(gameStr.substring(j, j + 2)));
                    }
                    games.push(nums);
                }

                const gameLabels = ['A', 'B', 'C', 'D', 'E'];

                games.forEach((myNums, idx) => {
                    let matchCount = 0;
                    let bonusMatch = false;

                    myNums.forEach(n => {
                        if (mainNums.includes(n)) matchCount++;
                        if (n === bonusNum) bonusMatch = true;
                    });

                    let rank = "낙첨";
                    let rankClass = "prize-none";

                    if (matchCount === 6) { rank = "1등 🥇"; rankClass = "prize-win"; }
                    else if (matchCount === 5 && bonusMatch) { rank = "2등 🥈"; rankClass = "prize-win"; }
                    else if (matchCount === 5) { rank = "3등 🥉"; rankClass = "prize-win"; }
                    else if (matchCount === 4) { rank = "4등 💵"; rankClass = "prize-win"; }
                    else if (matchCount === 3) { rank = "5등 💰"; rankClass = "prize-win"; }

                    // Render
                    const row = document.createElement('div');
                    row.className = 'qr-game-row';

                    const ballsHtml = myNums.map(n => {
                        let style = "display:inline-block; width:20px; text-align:center;";
                        let color = "#333";
                        let weight = "normal";

                        if (mainNums.includes(n)) {
                            color = "#d32f2f"; weight = "bold";
                        } else if (n === bonusNum && matchCount === 5) {
                            color = "#1976d2"; weight = "bold"; // Bonus highlight
                        }

                        return `<span style="${style} color:${color}; font-weight:${weight};">${n}</span>`;
                    }).join('');

                    row.innerHTML = `
                        <div style="font-weight:bold; color:#666; width:20px;">${gameLabels[idx] || '?'}</div>
                        <div style="flex:1; display:flex; justify-content:center; gap:2px; font-size:13px;">
                            ${ballsHtml}
                        </div>
                        <div class="qr-prize-badge ${rankClass}">${rank}</div>
                    `;
                    listContainer.appendChild(row);
                });

            } catch (e) {
                console.error(e);
                alert("QR 코드를 분석할 수 없습니다. " + e.message);
                restartQRScanner();
            }
        }

        // Close modal when clicking outside (click + touchstart for mobile)
        const handleBackdropClick = (event) => {
            const adModal = document.getElementById('adModal');
            const statModal = document.getElementById('statModal');
            const qrModal = document.getElementById('qrModal');
            if (event.target === adModal) {
                closeModal();
            }
            if (event.target === statModal) {
                closeStatModal();
            }
            if (event.target === qrModal) {
                closeQRScanner();
            }
        };

        window.addEventListener('click', handleBackdropClick);
        window.addEventListener('touchstart', handleBackdropClick, { passive: true });

        // Handle Back Button
        window.addEventListener('popstate', function (event) {
            // When history changes (Back pressed), we close the modal UI
            // Check if modal is currently visible
            const modal = document.getElementById('adModal');
            if (modal && modal.style.display === 'flex') {
                _internalCloseModal();
            }
        });



        function focusShop(lat, lng) {
            console.log('Focusing shop:', lat, lng);
            // Find marker by coordinates (approximate match to handle float precision)
            const target = markers.find(m => {
                const p = m.getPosition();
                return Math.abs(p.getLat() - lat) < 0.0001 && Math.abs(p.getLng() - lng) < 0.0001;
            });

            if (target) {
                // Zoom in to resolve clusters and ensure marker is visible
                if (map.getLevel() > 5) {
                    map.setLevel(3);
                }
                const mapCenter = new kakao.maps.LatLng(lat, lng);
                map.panTo(mapCenter);

                // Trigger click to open InfoWindow (Wait a bit for pan to finish for better UI)
                setTimeout(() => {
                    kakao.maps.event.trigger(target, 'click');
                }, 300);
            } else {
                console.warn('Marker not found for:', lat, lng);
                showToast("현재 조건(회차 필터 등)에 맞는 판매점 마커를 찾을 수 없습니다.", "info");
            }
        }

        function findNearestShop(lat, lng, label = "내 위치", shouldPan = true) {
            // Find nearest among ACTIVE markers (filtered ones on the map)
            if (!markers || markers.length === 0) {
                // If it's a map drag, don't show toast if no markers. 
                // Only show if it's a specific request or shouldn't pan.
                if (shouldPan) showToast("현재 필터 조건에 부합하는 판매점이 지도에 없습니다.", "info");
                return;
            }

            // Sort all markers by distance
            const sortedByDist = markers.map(m => {
                const p = m.getPosition();
                return {
                    marker: m,
                    distance: getDistance(lat, lng, p.getLat(), p.getLng())
                };
            }).sort((a, b) => a.distance - b.distance);

            // Take top 3 (top 2 on mobile to prevent overlap)
            const isMobile = window.innerWidth <= 768;
            const topCount = isMobile ? 2 : 3;
            const topShops = sortedByDist.slice(0, topCount);
            if (topShops.length > 0) {
                // Check if the nearest shop is within a reasonable range (e.g., 20km)
                const nearestDist = topShops[0].distance;
                if (nearestDist > 20) {
                    if (shouldPan) {
                        showToast(`현재 조건(회차)으로는<br>주변 20km 내에 1등 당첨점이 없습니다.<br><span style="font-size:12px; color:#ccc;">(가장 가까운 곳: ${topShops[0].marker.shopData.n} ${nearestDist.toFixed(1)}km)</span>`, "info", true, 'nearby-shops-toast');

                        // Pan to user location but don't zoom out to the distant shop
                        const center = new kakao.maps.LatLng(lat, lng);
                        map.panTo(center);
                    }
                    return;
                }

                let msg = `📍 <strong style="white-space: nowrap;">${label} 주변 1등점</strong> <br class="mobile-br"> <strong>(가까운 순)</strong><br>`;
                topShops.forEach((item, index) => {
                    const shop = item.marker.shopData;
                    const distStr = item.distance < 1 ? Math.round(item.distance * 1000) + "m" : item.distance.toFixed(1) + "km";
                    // Add clickable span
                    msg += `<div onclick="focusShop(${shop.lat}, ${shop.lng})" style="cursor:pointer; padding:2px 0; text-decoration:underline;">${index + 1}. ${shop.n} (${distStr})</div>`;
                });

                if (shouldPan) {
                    // Adaptive Zoom: Fit my location and top nearest shops
                    const bounds = new kakao.maps.LatLngBounds();
                    bounds.extend(new kakao.maps.LatLng(lat, lng));

                    topShops.forEach(item => {
                        if (item.distance < 10) { // Only include within 10km for bounds
                            bounds.extend(item.marker.getPosition());
                        }
                    });

                    const bottomPad = isMobile ? 180 : 40;
                    map.setBounds(bounds, 40, 40, bottomPad, 40);
                }

                showToast(msg, "success", true, 'nearby-shops-toast'); // Use ID to prevent duplicates
            }
        }

        function showToast(message, type = "info", persistent = false, id = null) {
            const container = document.getElementById('toast-container');

            // Check for existing toast with same ID
            let toast = id ? document.getElementById(id) : null;

            if (toast && toast.parentNode === container) {
                // Update existing toast content
                const content = toast.querySelector('.toast-content');
                if (content) content.innerHTML = message;
                toast.className = `toast toast-${type} show`; // Ensure it's visible and has correct type
                return;
            }

            // Create new toast if not found
            toast = document.createElement('div');
            if (id) toast.id = id;
            toast.className = `toast toast-${type}`;

            // Contents
            const content = document.createElement('div');
            content.className = 'toast-content'; // Add class for update logic
            content.innerHTML = message;
            toast.appendChild(content);

            // Close Button
            const closeBtn = document.createElement('span');
            closeBtn.className = 'toast-close';
            closeBtn.innerHTML = '&times;';
            closeBtn.onclick = () => {
                toast.classList.remove('show');
                setTimeout(() => {
                    if (toast.parentNode === container) container.removeChild(toast);
                }, 300);
            };
            toast.appendChild(closeBtn);

            container.appendChild(toast);

            // Force reflow
            toast.offsetHeight;

            toast.classList.add('show');

            // Auto-hide only if NOT persistent
            if (!persistent) {
                setTimeout(() => {
                    if (toast.classList.contains('show')) {
                        toast.classList.remove('show');
                        setTimeout(() => {
                            if (toast.parentNode === container) container.removeChild(toast);
                        }, 300);
                    }
                }, 5000);
            }
        }

        // Helper to forcefully clear toasts
        function closeAllToasts() {
            const container = document.getElementById('toast-container');
            if (container) container.innerHTML = '';
        }

        function copyToClipboard(text) {
            const textarea = document.createElement('textarea');
            textarea.value = text;
            document.body.appendChild(textarea);
            textarea.select();
            try {
                document.execCommand('copy');
                showToast("📋 주소가 클립보드에 복사되었습니다.", "success");
            } catch (err) {
                showToast("복사 실패", "error");
            }
            document.body.removeChild(textarea);
        }

        function openDirections(lat, lng, name) {
            const url = `https://map.kakao.com/link/to/${encodeURIComponent(name)},${lat},${lng}`;
            window.open(url, '_blank');
        }

        function shareToKakao() {
            try {
                console.log('[Kakao Share] Function called');

                // Check if Kakao SDK is loaded
                if (typeof window.Kakao === 'undefined') {
                    console.error('[Kakao Share] Kakao SDK not loaded');
                    return;
                }

                console.log('[Kakao Share] Kakao SDK loaded successfully');

                // Initialize Kakao SDK if not already initialized
                if (!window.Kakao.isInitialized()) {
                    console.log('[Kakao Share] Initializing Kakao SDK...');
                    window.Kakao.init('a6b27b6dab16c7e3459bb9589bf1269d');
                    console.log('[Kakao Share] Kakao SDK initialized');
                } else {
                    console.log('[Kakao Share] Kakao SDK already initialized');
                }

                // Prepare share data - NO IMAGE to ensure k-inov.co.kr link works
                const shareData = {
                    objectType: 'feed',
                    content: {
                        title: '🎰 KINOV 로또 명당 지도',
                        description: '역대 1등 당첨 판매점을 한눈에! 당신의 행운을 찾아보세요.\n\n지금 바로 KINOV Mall을 방문하세요!',
                        link: {
                            mobileWebUrl: 'https://www.k-inov.co.kr',
                            webUrl: 'https://www.k-inov.co.kr'
                        }
                    },
                    buttons: [
                        {
                            title: 'KINOV Mall 방문하기',
                            link: {
                                mobileWebUrl: 'https://www.k-inov.co.kr',
                                webUrl: 'https://www.k-inov.co.kr'
                            }
                        }
                    ]
                };

                console.log('[Kakao Share] Sending share data:', shareData);

                // Send KakaoTalk share message
                window.Kakao.Share.sendDefault(shareData);

                console.log('[Kakao Share] Share dialog opened successfully');

            } catch (error) {
                console.error('[Kakao Share] Error:', error);
            }
        }
    