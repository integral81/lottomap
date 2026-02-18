import json
import sys

def audit_legends():
    try:
        with open('lotto_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        shops = {}
        for entry in data:
            addr = entry.get('a', 'unknown')
            name = entry.get('n', 'unknown')
            key = f"{addr}|{name}"
            
            if key not in shops:
                shops[key] = {
                    'name': name,
                    'addr': addr,
                    'wins': 0,
                    'pov': None
                }
            
            shops[key]['wins'] += 1
            # Update POV if found in any entry for this shop
            if entry.get('pov') and isinstance(entry['pov'], dict) and entry['pov'].get('id'):
                shops[key]['pov'] = entry['pov']
        
        legends = sorted([v for v in shops.values() if v['wins'] >= 10], key=lambda x: x['wins'], reverse=True)
        
        sys.stdout.reconfigure(encoding='utf-8')
        print(f"총 레전드 매장 (10회 이상 당첨): {len(legends)}곳")
        
        missing = [v for v in legends if not v['pov']]
        if not missing:
            print("\n✅ 모든 레전드 매장의 POV가 정상적으로 등록되어 있습니다.")
        else:
            print(f"\n❌ POV 미등록 레전드 매장: {len(missing)}곳")
            for m in missing:
                print(f"- [{m['wins']}회] {m['name']} ({m['addr']})")
                
        # Also check Gold shops for context
        gold = [v for v in shops.values() if 5 <= v['wins'] < 10]
        missing_gold = [v for v in gold if not v['pov']]
        print(f"\n--- 참고 (골드 매장: 5~9회 당첨) ---")
        print(f"총 골드 매장: {len(gold)}곳")
        print(f"POV 미등록 골드 매장: {len(missing_gold)}곳")

    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    audit_legends()
