import json

target_name = "세븐일레븐부산온천장역점"
target_lat = 35.22047
target_lng = 129.086585
target_wins = 3
target_msg = "📍 매장은 온천장역 역사(지하) 내부에 있습니다."

db_path = 'lotto_data.json'
js_path = 'lotto_data.js'

try:
    with open(db_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    new_data = []
    found_first = False
    updated_count = 0
    removed_count = 0
    
    for s in data:
        if s.get('n') == target_name:
            if not found_first:
                # Update the first occurrence
                s['lat'] = target_lat
                s['lng'] = target_lng
                s['wins'] = target_wins
                s['customMessage'] = target_msg
                # Ensure it's not closed or hidden
                s['closed'] = False
                s['hidden'] = False
                new_data.append(s)
                found_first = True
                updated_count += 1
            else:
                # Skip duplicate occurrences
                removed_count += 1
        else:
            new_data.append(s)
            
    if updated_count > 0:
        with open(db_path, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, ensure_ascii=False, indent=0, separators=(',', ':'))
            
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write('var lottoData = ' + json.dumps(new_data, ensure_ascii=False, indent=0, separators=(',', ':')) + ';')
            
        print(f"Fixed Oncheonjang: Updated 1 entry, Removed {removed_count} duplicates.")
    else:
        print("Shop not found.")
        
except Exception as e:
    print(f"Error: {e}")
