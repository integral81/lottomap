
import json

def find_gapan():
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    for item in data:
        if "가판점" in item['n'] or "신도림" in item['a']:
            print(f"Found: {item['n']} | {item['a']} | POV: {item.get('pov') is not None}")

if __name__ == "__main__":
    find_gapan()
