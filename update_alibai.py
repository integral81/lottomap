import json

# Load data
with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Update rule
name = '알리바이'
addr = '광주 광산구 수등로'
pov_data = {
    'id': '1199874246',
    'pan': 106.07,
    'tilt': -6.88,
    'zoom': -3
}

# Update
count = 0
for item in data:
    if name in item['n'] and addr in item['a']:
        item['pov'] = pov_data
        count += 1

# Save
with open('lotto_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'Updated {count} records')
print(f'{name}: PanoID {pov_data["id"]} (pan: {pov_data["pan"]}, tilt: {pov_data["tilt"]}, zoom: {pov_data["zoom"]})')
