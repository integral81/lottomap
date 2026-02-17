import json

with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("Checking '훼미리로또'...")
fam = next((s for s in data if '훼미리로또' in s.get('n', '')), None)
if fam:
    print(f"Name: {fam.get('n')}")
    print(f"POV: {fam.get('pov')}")
    print(f"Message: {fam.get('roadview_msg')}")
else:
    print("Family Lotto: Not Found")

print("-" * 20)

print("Checking '승리복권판매점'...")
vic = next((s for s in data if '승리복권판매점' in s.get('n', '')), None)
if vic:
    print(f"Name: {vic.get('n')}")
    print(f"Coords: {vic.get('lat')}, {vic.get('lng')}")
else:
    print("Victory Lotto: Not Found")
