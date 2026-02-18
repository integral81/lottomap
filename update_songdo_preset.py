import os

path = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\index.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

new_preset = '{ name: "송도하우스", addr: "전남 목포시 영산로 525 목포터미널 내", panoId: 1192393715, pov: { pan: 292.18, tilt: 3.38, zoom: -3 } },'

insert_pos = content.find("const ROADVIEW_PRESETS = [")
if insert_pos != -1:
    opening_bracket_pos = content.find("[", insert_pos)
    new_content = content[:opening_bracket_pos+1] + "\n            " + new_preset + content[opening_bracket_pos+1:]
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Updated index.html.")
else:
    print("ROADVIEW_PRESETS not found.")
