import os

path = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\index.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

new_presets = [
    '{ name: "가자복권천국", addr: "전남 목포시 상동 878-4", panoId: 1192597080, pov: { pan: 53.56, tilt: 5.29, zoom: -1 } },',
    '{ name: "대풍로또판매점", addr: "경남 김해시 번화2로 36", panoId: 1194232894, pov: { pan: 241.96, tilt: -0.98, zoom: -3 } },'
]

insert_pos = content.find("const ROADVIEW_PRESETS = [")
if insert_pos != -1:
    opening_bracket_pos = content.find("[", insert_pos)
    
    presets_block = "\n            " + "\n            ".join(new_presets)
    new_content = content[:opening_bracket_pos+1] + presets_block + content[opening_bracket_pos+1:]
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Updated index.html.")
else:
    print("ROADVIEW_PRESETS not found.")
