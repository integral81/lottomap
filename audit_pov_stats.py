
import json
import os

def audit_pov():
    data_path = 'index.html'
    # Try to find lottoHistory in index.html or lotto_data.json
    # Since we restored to a stable state where it's likely linked to lotto_data.json
    
    try:
        with open('lotto_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading lotto_data.json: {e}")
        return

    # Group by name + address
    shops = {}
    for entry in data:
        # Ignore internet lotto
        if entry.get('n') == '인터넷 복권판매사이트' or entry.get('a') == '동행복권':
            continue
            
        key = (entry.get('n'), entry.get('a'))
        if key not in shops:
            shops[key] = {
                'name': entry.get('n'),
                'addr': entry.get('a'),
                'wins': 0,
                'has_pov': False
            }
        
        shops[key]['wins'] += 1
        
        pov = entry.get('pov')
        if pov and isinstance(pov, dict):
            pov_id = pov.get('id')
            if pov_id and not str(pov_id).startswith('SKIP'):
                shops[key]['has_pov'] = True
        elif entry.get('panoid'): # Some versions use panoid directly
            shops[key]['has_pov'] = True

    # Stats
    stats = {
        '4+': {'total': 0, 'missing_pov': 0, 'missing_list': []},
        '3': {'total': 0, 'missing_pov': 0},
        '2': {'total': 0, 'missing_pov': 0},
        '1': {'total': 0, 'missing_pov': 0},
        '0': {'total': 0, 'missing_pov': 0}
    }

    for shop in shops.values():
        wins = shop['wins']
        category = str(wins) if wins < 4 else '4+'
        
        if category not in stats:
            category = '0' # Should not happen with wins >= 1
            
        stats[category]['total'] += 1
        if not shop['has_pov']:
            stats[category]['missing_pov'] += 1
            if category == '4+':
                stats[category]['missing_list'].append(f"{shop['name']} ({shop['addr']}) - {wins}회")

    print("\n=== POV 등록 현황 분석 결과 ===")
    print(f"대상 점포 수: {len(shops)}개 (인터넷 판매처 제외)")
    print("-" * 30)
    
    for cat in ['4+', '3', '2', '1']:
        s = stats[cat]
        print(f"[{cat}회 당첨] 전체: {s['total']} / POV 미등록: {s['missing_pov']}")
        
    sorted_missing = sorted(stats['4+']['missing_list'], key=lambda x: int(x.split('-')[-1].replace('회','')), reverse=True)
    
    # Generate JSON for admin_pov.html
    targets = []
    for item in sorted_missing:
        # Extract name and address from the string "Name (Address) - Wins회"
        try:
            name_part, rest = item.split(' (', 1)
            addr_part, win_part = rest.split(') - ', 1)
            targets.append({
                "n": name_part,
                "a": addr_part,
                "w": int(win_part.replace('회', ''))
            })
        except:
            continue
            
    with open('targets_for_admin.json', 'w', encoding='utf-8') as f:
        json.dump(targets, f, ensure_ascii=False, indent=4)
    print(f"\n{len(targets)}개의 타겟 정보가 'targets_for_admin.json'에 저장되었습니다.")

if __name__ == "__main__":
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    audit_pov()
