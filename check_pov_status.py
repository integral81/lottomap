import json

targets = ['제철', 'Goodday', '완월', '채널큐', '해피복권', '세븐', '온천장']

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Total entries: {len(data)}")
    
    for t in targets:
        print(f"\nChecking key '{t}':")
        found = [s for s in data if t in s.get('n', '')]
        if not found:
            print(f"  No entries found matching '{t}'")
        for s in found:
            has_pov = s.get('pov')
            has_panoid = s.get('panoid')
            print(f"  {s['n']} ({s['a']}): POV={bool(has_pov)}, Pano={has_panoid}, Round={s.get('r')}")

except Exception as e:
    print(e)
