
import json

# Load data
with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Update Metro Center Point
count = 0
for item in data:
    if "메트로센터점" in item['n']:
        # Add img field and POV marker
        item['img'] = "assets/img/metro_260213.jpg"
        item['pov'] = {"id": "IMG_REGISTERED", "pan": 0, "tilt": 0, "zoom": 0}
        count += 1

# Save
with open('lotto_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Updated {count} records for Metro Center Point with image")
