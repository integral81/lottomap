
import json

target_file = 'lotto_data.json'
new_name = '오케이상사'

try:
    with open(target_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Define matches for consolidation
    # 1. Name contains '오케이상사' or '센트럴시티'
    # 2. Address contains '반포동 19-3' or '신반포로 176'
    
    matches = []
    others = []
    
    for item in data:
        name = item.get('n', '')
        addr = item.get('a', '')
        
        is_match = False
        if '오케이상사' in name or '센트럴시티' in name:
            is_match = True
        elif '신반포로 176' in addr or '반포동 19-3' in addr:
            # Exclude other stores if necessary, but usually these are the same winner cluster
            if '오케이상사' in name or '센트럴시티' in name or '씨티' in name:
                is_match = True
            elif addr.strip() == '서울 서초구 반포동 19-3' and name == '오케이상사': # Exact match from user request
                 is_match = True
                 
        if is_match:
            matches.append(item)
        else:
            others.append(item)
            
    print(f'Total entries: {len(data)}')
    print(f'Matches found for consolidation: {len(matches)}')
    
    if matches:
        # Create consolidated entry
        # Prefer the one with user-provided name or the most common coordinates
        representative = matches[0].copy()
        representative['n'] = new_name
        # Use coordinates from index.html if possible or first match
        # Index.html coords for 센트럴시티빌딩: lat 37.503935..., lng 127.002413...
        representative['lat'] = 37.5039351769908
        representative['lng'] = 127.002413006799
        representative['a'] = '서울 서초구 신반포로 176 (반포동)'
        
        others.append(representative)
        print(f'Consolidated {len(matches)} entries into 1.')
        
        with open(target_file, 'w', encoding='utf-8') as f:
            json.dump(others, f, ensure_ascii=False, indent=2)
        print('Successfully updated lotto_data.json.')
    else:
        print('No matches found to consolidate.')

except Exception as e:
    print(f'Error: {e}')
