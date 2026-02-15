
import json

def find_happy():
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    targets = ["\ud589\ubcfc\ud55c\uc0ac\ub78c\ub4e4"] # 행복한사람들
    
    results = {}
    for e in data:
        n = e.get('n', '')
        if targets[0] in n:
            k = f"{n}|{e.get('a', '')}"
            if k not in results:
                results[k] = {"n": n, "a": e.get('a', ''), "w": 0, "lat": e.get('lat'), "lng": e.get('lng')}
            results[k]["w"] += 1
            
    for s in results.values():
        print(f"[{s['w']} wins] {s['n']} | {s['a']} | {s['lat']}, {s['lng']}")

if __name__ == "__main__":
    find_happy()
