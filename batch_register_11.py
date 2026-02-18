import json
import os

db_path = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json"
js_path = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js"

if not os.path.exists(db_path):
    print(f"Error: {db_path} not found.")
    exit(1)

with open(db_path, "r", encoding="utf-8") as f:
    data = json.load(f)

new_povs = [
    { "name": "가로판매점", "addr": "서울 영등포구 양평로 46 가판", "panoid": "1198119684", "pov": { "pan": 348.99, "tilt": 17.73, "zoom": -3 } },
    { "name": "복권천국", "addr": "경기 광명시 기아로 6", "panoid": "1203492434", "pov": { "pan": 183.47, "tilt": 9.63, "zoom": -1 } },
    { "name": "로또명당인주점", "addr": "충남 아산시 인주면 서해로 519-2", "panoid": "1152034899", "pov": { "pan": 320.94, "tilt": 2.29, "zoom": -3 } },
    { "name": "돈벼락맞는곳", "addr": "부산 해운대구 양운로 55 두산위브센티움상가102호", "panoid": "1202542572", "pov": { "pan": 358.50, "tilt": 4.14, "zoom": 0 } },
    { "name": "천하명당", "addr": "경기 파주시 방촌로 1719-68 좋은빌딩2 107호", "panoid": "1175741916", "pov": { "pan": 333.86, "tilt": 7.02, "zoom": -3 } },
    { "name": "대박찬스", "addr": "충북 청주시 흥덕구 가경로161번길 3", "panoid": "1170563610", "pov": { "pan": 245.56, "tilt": 2.95, "zoom": 0 } },
    { "name": "로또명당", "addr": "경기 남양주시 진접읍 장현리 84-3", "panoid": "1202943251", "pov": { "pan": 265.18, "tilt": -5.55, "zoom": 3 } },
    { "name": "로또", "addr": "경기 포천시 죽엽산로196번길 4", "panoid": "1175927134", "pov": { "pan": 355.87, "tilt": 0.20, "zoom": 3 } },
    { "name": "일등복권편의점", "addr": "대구 달서구 본리동 2-16번지 1층", "panoid": "1201526676", "pov": { "pan": 345.04, "tilt": 6.19, "zoom": 0 } },
    { "name": "로또휴게실", "addr": "경기 용인시 기흥구 용구대로 1885", "panoid": "1199447820", "pov": { "pan": 276.39, "tilt": 2.24, "zoom": 1 } },
    { "name": "복권왕국", "addr": "인천 부평구 부흥로 359", "panoid": "1199223234", "pov": { "pan": 27.14, "tilt": 9.55, "zoom": 1 } },
    { "name": "대박로또", "addr": "대전 중구 대종로 174", "panoid": "1201508154", "pov": { "pan": 66.16, "tilt": 5.67, "zoom": 3 } },
    { "name": "복권백화점", "addr": "경기 파주시 금촌2동 329-135", "panoid": "1202862937", "pov": { "pan": 88.79, "tilt": -2.28, "zoom": -3 } },
    { "name": "주택복권방", "addr": "경기 용인시 수지구 풍덕천동 717-3 103호", "panoid": "1199750330", "pov": { "pan": 141.71, "tilt": 4.33, "zoom": 0 } }
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
