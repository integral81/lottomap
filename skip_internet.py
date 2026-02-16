
import json

# Load data
with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Skip Internet Lotto Site
count = 0
for item in data:
    if "인터넷 복권판매사이트" in item['n']:
        item['pov'] = {"id": "SKIP_INTERNET", "pan": 0, "tilt": 0, "zoom": 0}
        count += 1

# Save
with open('lotto_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Skipped {count} records for Internet Lotto Site")
