
import json

def final_check():
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Shop 3: 메트로센터점
    # Shop 4: 행복한사람들
    
    queries = [
        {"name": "Metro (Deoksan)", "keywords": ["덕산동 88"]},
        {"name": "Metro (Dalgubeol)", "keywords": ["달구벌대로 지하 2100"]},
        {"name": "Happy (Saniri)", "keywords": ["산이리 13-1"]},
        {"name": "Happy (Gyeongchung)", "keywords": ["경충대로 763"]}
    ]
    
    for q in queries:
        count = 0
        names = set()
        for e in data:
            a = e.get('a', '')
            match = False
            for k in q["keywords"]:
                if k in a:
                    match = True
                    break
            if match:
                count += 1
                names.add(e.get('n', ''))
        print(f"{q['name']}: {count} wins. Found names: {list(names)}")

if __name__ == "__main__":
    final_check()
