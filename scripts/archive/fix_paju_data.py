import json

def fix_data():
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Correct values
    correct_name = "대박행진복권랜드"
    correct_addr = "경기 파주시 금촌동 989-1 금촌프라자 107호"
    
    # Fragments to identify the shop
    identifying_fragments = ["16호금촌프라자107", "989-1", "금촌2택지사업지구"]
    
    count = 0
    for item in data:
        for frag in identifying_fragments:
            if frag in item['a']:
                item['n'] = correct_name
                item['a'] = correct_addr
                count += 1
                break
                
    with open('lotto_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print(f"Updated {count} entries in lotto_data.json")

    # Also fix admin_targets.json
    with open('admin_targets.json', 'r', encoding='utf-8') as f:
        targets = json.load(f)
    
    t_count = 0
    for item in targets:
        for frag in identifying_fragments:
            if frag in item['address']:
                item['name'] = correct_name
                item['address'] = correct_addr
                t_count += 1
                break
                
    with open('admin_targets.json', 'w', encoding='utf-8') as f:
        json.dump(targets, f, ensure_ascii=False, indent=4)
        
    print(f"Updated {t_count} targets in admin_targets.json")

if __name__ == "__main__":
    fix_data()
