import json
import os

db_path = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json"
js_path = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js"

with open(db_path, "r", encoding="utf-8") as f:
    data = json.load(f)

new_povs = [
    { "name": "로또복권방", "addr": "충북 청주시 청원구 내수로 725-1 디지털프라자 옆", "panoid": "1169985988", "pov": { "pan": 311.72, "tilt": -0.13, "zoom": -3 } },
    { "name": "천하명당복권방", "addr": "충남 홍성군 홍성읍 오관리 321-4", "panoid": "1161022469", "pov": { "pan": 191.04, "tilt": 8.65, "zoom": 2 } },
    { "name": "행운복권", "addr": "서울 영등포구 도신로65길 2 1층", "panoid": "1175680167", "pov": { "pan": 316.48, "tilt": -4.71, "zoom": 1 } },
    { "name": "스파", "addr": "서울 노원구 동일로 1493", "panoid": "1198397843", "pov": { "pan": 294.76, "tilt": 8.92, "zoom": 0 } },
    { "name": "대박복권방", "addr": "경기 안산시 단원구 신길중앙로1길 40 101호", "panoid": "1204111998", "pov": { "pan": 38.82, "tilt": 9.60, "zoom": 1 } },
    { "name": "부일카서비스", "addr": "부산 동구 자성로133번길 35", "panoid": "1202519412", "pov": { "pan": 237.14, "tilt": 6.15, "zoom": -2 } }
]

modified_names = set()
for pov in new_povs:
    count = 0
    for s in data:
        # Flexible matching for name and address
        if pov["name"] in s["n"] and (pov["addr"][:10] in s["a"] or s["a"][:10] in pov["addr"]):
            s["pov"] = {
                "id": str(pov["panoid"]),
                "pan": pov["pov"]["pan"],
                "tilt": pov["pov"]["tilt"],
                "zoom": pov["pov"]["zoom"]
            }
            count += 1
    if count > 0:
        modified_names.add(pov["name"])
    print(f"Updated {pov['name']}: {count} entries.")

with open(db_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=0, separators=(",", ":"), ensure_ascii=False)

js_content = "var lottoData = " + json.dumps(data, ensure_ascii=False, indent=0, separators=(",", ":")) + ";"
with open(js_path, "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"Total shops updated: {len(modified_names)}")
