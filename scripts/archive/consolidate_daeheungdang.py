import json

def consolidate_daeheungdang():
    # 1. Update lotto_data.json
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    old_addr = "시기동 413-6"
    new_addr = "전북 정읍시 관통로 102"
    
    count = 0
    for item in data:
        # Check if it's Daeheungdang at the old address
        if old_addr in item['a'] and "대흥당" in item['n']:
            item['a'] = new_addr
            count += 1
                
    with open('lotto_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Updated {count} entries in lotto_data.json")

    # 2. Update admin_targets.json
    with open('admin_targets.json', 'r', encoding='utf-8') as f:
        targets = json.load(f)
    
    t_count = 0
    for item in targets:
        if old_addr in item['address']:
            item['address'] = new_addr
            t_count += 1
                
    with open('admin_targets.json', 'w', encoding='utf-8') as f:
        json.dump(targets, f, ensure_ascii=False, indent=4)
    print(f"Updated {t_count} targets in admin_targets.json")

if __name__ == "__main__":
    consolidate_daeheungdang()
