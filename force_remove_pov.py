import json

# 1. Load Data
src_file = 'lotto_data.json'
with open(src_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 2. Force Remove POV for Sky Lotto
target_name = "하늘로또"
target_addr = "세종로475번길 2"

updated = False
for shop in data:
    if target_name in shop['n'] and target_addr in shop['a']:
        if 'pov' in shop:
            del shop['pov']
            print(f"Removed POV for {shop['n']}")
            updated = True
        else:
            print(f"POV already missing for {shop['n']}")

# 3. Save
if updated:
    with open(src_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Saved lotto_data.json")
else:
    print("No changes made.")
