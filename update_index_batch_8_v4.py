import os

path = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\index.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

new_presets = """
            { name: "구포라인점", addr: "부산 북구 구포동 700-148", panoId: 1202526432, pov: { pan: 255.82, tilt: 3.43, zoom: 1 } },
            { name: "영화복권", addr: "경남 창원시 진해구 안청남로 14", panoId: 1204354980, pov: { pan: 175.08, tilt: 0.44, zoom: 1 } },
            { name: "로또구포점", addr: "부산 북구 덕천2길 23-3", panoId: 1202240178, pov: { pan: 2.70, tilt: 1.64, zoom: -3 } },
            { name: "큐마트학동점로또", addr: "전남 여수시 학동서5길 2 큐마트내", panoId: 1131607851, pov: { pan: 298.29, tilt: -8.06, zoom: 0 } },
            { name: "씨스페이스(범어사역점)", addr: "부산 금정구 남산동 21-4", panoId: 1202570280, pov: { pan: 268.49, tilt: 3.29, zoom: 1 } },
            { name: "우리로또복권방", addr: "전남 여수시 무선중앙로 71", panoId: 1205657400, pov: { pan: 358.65, tilt: 8.13, zoom: 1 } },
            { name: "천하복권방", addr: "울산 동구 전하로 29", panoId: 1202146730, pov: { pan: 219.93, tilt: -1.81, zoom: -3 } },
            { name: "일레븐마트무선점", addr: "전남 여수시 성산로 19", panoId: 1205608266, pov: { pan: 327.53, tilt: -3.95, zoom: -3 } },"""

# Inserting at the beginning of ROADVIEW_PRESETS array
insert_pos = content.find("const ROADVIEW_PRESETS = [")
if insert_pos != -1:
    opening_bracket_pos = content.find("[", insert_pos)
    new_content = content[:opening_bracket_pos+1] + new_presets + content[opening_bracket_pos+1:]
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Updated index.html presets for Batch 4.")
else:
    print("ROADVIEW_PRESETS not found in index.html.")
