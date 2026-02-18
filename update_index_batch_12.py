import os

path = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\index.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

new_presets = """
            { name: "운수대통", addr: "경기 군포시 군포로745번길 24", panoId: 1175676242, pov: { pan: 321.44, tilt: 4.25, zoom: -3 } },
            { name: "인더라인 로또", addr: "인천 부평구 십정동 577-6", panoId: 1198797088, pov: { pan: 283.28, tilt: -0.18, zoom: 0 } },
            { name: "행운마트", addr: "인천 동구 송림로 71-1", panoId: 1199336752, pov: { pan: 338.98, tilt: -1.36, zoom: -2 } },
            { name: "영화유통(1등복권방)", addr: "경북 포항시 북구 양학천로 15", panoId: 1187457532, pov: { pan: 32.63, tilt: -4.20, zoom: 0 } },"""

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
