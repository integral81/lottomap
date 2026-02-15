import json

def check():
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    targets = [
        "홍성읍 321-4",
        "독산동 1090-7", 
        "권선동 1295-3",
        "완산구 서노송동 749-1",
        "송산면 유곡리 876-2" 
    ]
    
    found = []
    for item in data:
        for t in targets:
            if t in item['a']:
                found.append(item)
                break
                
    for item in found:
        print(f"Name: [{item['n']}]")
        print(f"Hex Name: {' '.join(hex(ord(c)) for c in item['n'])}")
        print(f"Addr: [{item['a']}]")
        print("-" * 20)

if __name__ == "__main__":
    check()
