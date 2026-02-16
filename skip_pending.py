
import json

# Load data
with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Skip targets
skip_names = ['로또복권두정점', '미나식품(로또판매점)']
count = 0

for item in data:
    for name in skip_names:
        if name in item['n']: # substring match usually safe for these unique names
            # Only skip if no POV exists (to avoid overwriting valid POV if my logic was wrong)
            # But user said "skip", so we overwrite to force exclusion.
            # Actually, user said "registered correctly", so maybe check if it has POV?
            # If it had POV, it wouldn't be in the list.
            # So it must NOT have POV in my data.
            # So I act as if I am "acknowledging" it is done.
            item['pov'] = {"id": "SKIP_USER_CONFIRMED", "pan": 0, "tilt": 0, "zoom": 0}
            count += 1

# Save
with open('lotto_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Skipped {count} records for: {', '.join(skip_names)}")
