import os

path = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\index.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

new_presets = [
    '{ name: "서창복권나라", addr: "경남 양산시 서창서2길 3", panoId: 1204300634, pov: { pan: 196.63, tilt: 0.83, zoom: -3 } },',
    '{ name: "드림복권", addr: "경남 김해시 부곡동 809-3", panoId: 1194474379, pov: { pan: 225.66, tilt: 1.54, zoom: -2 } },',
    '{ name: "대동복권방", addr: "경남 김해시 월산로 112-57 이마트편의점 좌측 복권판매점", panoId: 1194481723, pov: { pan: 323.09, tilt: 3.41, zoom: 1 } },',
    '{ name: "CU(달동초이스점)", addr: "울산 남구 달동 1309-1", panoId: 1202053722, pov: { pan: 92.21, tilt: -1.20, zoom: -3 } },'
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
