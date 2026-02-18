import os

path = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\index.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

new_preset = '{ name: "대박상사", addr: "경남 창원시 진해구 충장로 88 (석동)", panoId: 1204704456, pov: { pan: 4.5, tilt: 5.7, zoom: 0 } },'

insert_pos = content.find("const ROADVIEW_PRESETS = [")
if insert_pos != -1:
    opening_bracket_pos = content.find("[", insert_pos)
    new_content = content[:opening_bracket_pos+1] + "\n            " + new_preset + content[opening_bracket_pos+1:]
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Updated index.html.")
else:
    print("ROADVIEW_PRESETS not found.")
