import json
import sys

# Set output encoding to utf-8
sys.stdout.reconfigure(encoding='utf-8')

with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for s in data:
    if "세븐일레븐부산온천장역점" in s.get('n', ''):
        print(f"Name: {s.get('n')}")
        print(f"Lat: {s.get('lat')}, Lng: {s.get('lng')}")
        print(f"Wins: {s.get('wins', 'N/A')}")
        print(f"Closed: {s.get('closed', False)}")
        print(f"Hidden: {s.get('hidden', False)}")
        # Print customMessage safely
        msg = s.get('customMessage', 'None')
        print(f"CustomMsg: {msg}")
        print("-" * 20)
