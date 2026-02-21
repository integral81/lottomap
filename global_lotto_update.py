import json
import re
import os

# 1. Update lotto_data files (Donghaeng HQ wins to 106)
dhl_hq_new = {
    "n": "동행복권(dhlottery.co.kr)",
    "a": "서울특별시 서초구 남부순환로 2423 한원빌딩",
    "lat": 37.485189,
    "lng": 127.013531,
    "w": 106,
    "totalWins": 106,
    "rounds": [{"r": (1211 - i), "m": "사이트"} for i in range(106)]
}

files = ["lotto_data.js", "lotto_data.json"]
for file in files:
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
        
        if file == "lotto_data.js":
            match = re.search(r"const lottoData = (\[.*\]);", content, re.DOTALL)
            data = json.loads(match.group(1))
        else:
            data = json.loads(content)
        
        # Replace Donghaeng HQ
        data = [item for item in data if not ("동행복권" in item.get("n", "") and "서초" in item.get("a", ""))]
        data.append(dhl_hq_new)
        
        if file == "lotto_data.js":
            updated = f"const lottoData = {json.dumps(data, ensure_ascii=False, indent=4)};"
            with open(file, "w", encoding="utf-8") as f:
                f.write(updated)
        else:
            with open(file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Updated Donghaeng HQ wins to 106 in {file}")

# 2. Update all Python scripts (Excel reference)
old_name = "lotto_cutted data final.xlsx"
new_name = "lotto_cutted data final.xlsx"

for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            if old_name in content:
                updated = content.replace(old_name, new_name)
                # Also ensure Sheet1 reference if relevant (usually default in pandas)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(updated)
                print(f"Updated Excel reference in {file}")

print("Global source and data update complete.")
