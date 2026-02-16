
import json
import math
from collections import defaultdict

def haversine_distance(lat1, lng1, lat2, lng2):
    """Calculate distance between two points in meters"""
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lng2 - lng1)
    a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def consolidate_duplicates():
    """Automatically consolidate validated duplicate shops"""
    print("Loading lotto_data.json...")
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Backup
    print("Creating backup...")
    with open('lotto_data_before_consolidation.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # Define consolidation rules (from analysis)
    consolidation_rules = [
        {
            'name': '복권나라',
            'main_address': '인천 남구 용현동 611-1',
            'merge_addresses': ['인천 미추홀구 토금북로 47']
        },
        {
            'name': '25시슈퍼',
            'main_address': '경기 시흥시 정왕동 1882-11번지 홍익프라자1층107호',
            'merge_addresses': ['함송로14번길 13-17']
        },
        {
            'name': '로또복권방',
            'main_address': '세종 용포로 32',
            'merge_addresses': ['세종 금남면 용포리 85-1']
        }
    ]
    
    total_consolidated = 0
    consolidation_log = []
    
    for rule in consolidation_rules:
        shop_name = rule['name']
        main_addr = rule['main_address']
        merge_addrs = rule['merge_addresses']
        
        # Find main address record to get lat/lng
        main_record = None
        for item in data:
            if item['n'] == shop_name and item['a'] == main_addr:
                main_record = item
                break
        
        if not main_record:
            print(f"Warning: Main address not found for {shop_name}")
            continue
        
        main_lat = main_record.get('lat', 0)
        main_lng = main_record.get('lng', 0)
        
        # Consolidate
        consolidated_count = 0
        for item in data:
            if item['n'] == shop_name and item['a'] in merge_addrs:
                # Update address to main address
                old_addr = item['a']
                item['a'] = main_addr
                item['lat'] = main_lat
                item['lng'] = main_lng
                consolidated_count += 1
        
        if consolidated_count > 0:
            log_entry = {
                'shop_name': shop_name,
                'main_address': main_addr,
                'merged_addresses': merge_addrs,
                'records_updated': consolidated_count
            }
            consolidation_log.append(log_entry)
            total_consolidated += consolidated_count
            
            print(f"\n✓ {shop_name}")
            print(f"  Main: {main_addr}")
            for addr in merge_addrs:
                print(f"  Merged: {addr}")
            print(f"  Records updated: {consolidated_count}")
    
    # Save consolidated data
    with open('lotto_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # Save log
    with open('consolidation_log.json', 'w', encoding='utf-8') as f:
        json.dump(consolidation_log, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*80}")
    print(f"CONSOLIDATION COMPLETE")
    print(f"{'='*80}")
    print(f"Total records consolidated: {total_consolidated}")
    print(f"Shops consolidated: {len(consolidation_log)}")
    print(f"\nBackup saved to: lotto_data_before_consolidation.json")
    print(f"Log saved to: consolidation_log.json")
    print(f"{'='*80}\n")
    
    # Regenerate admin list
    print("Regenerating admin_targets.js...")
    import subprocess
    subprocess.run(['python', 'generate_admin_list_final.py'], check=True)
    
    return consolidation_log

if __name__ == "__main__":
    consolidate_duplicates()
