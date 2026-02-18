import os

path = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\index.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

new_presets = """
            { name: "로또복권방", addr: "충북 청주시 청원구 내수로 725-1 디지털프라자 옆", panoId: 1169985988, pov: { pan: 311.72, tilt: -0.13, zoom: -3 } },
            { name: "천하명당복권방", addr: "충남 홍성군 홍성읍 오관리 321-4", panoId: 1161022469, pov: { pan: 191.04, tilt: 8.65, zoom: 2 } },
            { name: "행운복권", addr: "서울 영등포구 도신로65길 2 1층", panoId: 1175680167, pov: { pan: 316.48, tilt: -4.71, zoom: 1 } },
            { name: "스파", addr: "서울 노원구 동일로 1493", panoId: 1198397843, pov: { pan: 294.76, tilt: 8.92, zoom: 0 } },
            { name: "대박복권방", addr: "경기 안산시 단원구 신길중앙로1길 40 101호", panoId: 1204111998, pov: { pan: 38.82, tilt: 9.60, zoom: 1 } },
            { name: "부일카서비스", addr: "부산 동구 자성로133번길 35", panoId: 1202519412, pov: { pan: 237.14, tilt: 6.15, zoom: -2 } },"""

# Inserting at the beginning of ROADVIEW_PRESETS array
insert_pos = content.find("const ROADVIEW_PRESETS = [")
if insert_pos != -1:
    opening_bracket_pos = content.find("[", insert_pos)
    new_content = content[:opening_bracket_pos+1] + new_presets + content[opening_bracket_pos+1:]
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Updated index.html presets.")
else:
    print("ROADVIEW_PRESETS not found in index.html.")
