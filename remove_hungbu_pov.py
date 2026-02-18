import json

db_path = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json"
js_path = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js"

with open(db_path, "r", encoding="utf-8") as f:
    data = json.load(f)

removed_count = 0
for item in data:
    if item.get("n") == "행복한사람들 (흥부네)":
        if "pov" in item:
            del item["pov"]
            removed_count += 1

with open(db_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=0)

with open(js_path, "w", encoding="utf-8") as f:
    f.write("var lottoData = " + json.dumps(data, ensure_ascii=False, indent=0) + ";")

print(f"Successfully removed POV from {removed_count} entries for '행복한사람들 (흥부네)'.")
