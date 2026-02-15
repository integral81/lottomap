import json

def consolidate_tier2_giants():
    json_path = 'lotto_data.json'
    
    # Tier 2 Consolidations based on previous audit
    consolidation_rules = [
        {
            "name": "일등복권편의점",
            "matches": ["대구", "달서구", "대명천로", "본리동"],
            "master_addr": "대구 달서구 대명천로 220 (본리동 2-16 1층)",
            "verify_pov_exists": True
        },
        {
            "name": "잠실매점",
            "matches": ["송파", "잠실", "올림픽로"],
            "master_addr": "서울 송파구 올림픽로 269 잠실역 8번출구 앞 (신천동 7-18)",
            "verify_pov_exists": True
        },
        {
            "name": "라이프마트",
            "matches": ["인천", "중구", "항동", "연안부두로"], # 인천 중구 항동7가 58-98 vs 연안부두로 53번길 36
            "master_addr": "인천 중구 연안부두로53번길 36 (항동7가 58-98 5호)",
            "verify_pov_exists": True
        }
        # Add more as we identify them from the audit list
    ]
    
    # Let's run a quick audit to find candidates for this script first?
    # Actually, let's just use the logic from audit again but apply consolidation where names match and 3+ wins total.
    
    # Logic: Group by Name + Region (City/Gu). If multiple addresses exist and total wins >= 3, merge to the one with POV or latest.
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Group by (Name, Region_Prefix)
        groups = {}
        for item in data:
            if not item.get('n'): continue
            name = item['n']
            # Region prefix: First 2 words of address? e.g. "서울 노원구"
            addr_parts = item.get('a', '').split()
            if len(addr_parts) >= 2:
                region = " ".join(addr_parts[:2])
            else:
                region = "Unknown"
            
            key = (name, region)
            if key not in groups:
                groups[key] = []
            groups[key].append(item)
            
        total_merged_groups = 0
        total_records_updated = 0
        
        for key, items in groups.items():
            name, region = key
            
            # Check if multiple addresses exist
            addresses = set(i.get('a', '') for i in items)
            if len(addresses) > 1 and len(items) >= 3:
                # Potential consolidation candidate
                # Find best record (has POV, or most recent?)
                best_record = None
                # Prioritize record with POV
                for i in items:
                    if 'pov' in i and i['pov']:
                        best_record = i
                        break
                
                if not best_record:
                    # If no POV, rely on most recent round? (Assumes list is sorted or we verify 'r')
                    # Actually data isn't guaranteed sorted.
                    # Let's just pick the most frequent address?
                    # Or the one with Road Name address?
                    # For now, skip if no POV to be safe, OR merge to the one with "road name" format if possible.
                    continue
                
                # Consolidate to best_record
                master_addr = best_record.get('a')
                master_pov = best_record.get('pov')
                master_lat = best_record.get('lat')
                master_lng = best_record.get('lng')
                
                updated_count = 0
                for i in items:
                    if i.get('a') != master_addr:
                        i['a'] = master_addr
                        i['pov'] = master_pov
                        i['lat'] = master_lat
                        i['lng'] = master_lng
                        if 'closed' in i: del i['closed']
                        updated_count += 1
                
                if updated_count > 0:
                    print(f"Auto-consolidated {name} ({region}): {len(items)} records -> {master_addr}")
                    total_merged_groups += 1
                    total_records_updated += updated_count

        if total_records_updated > 0:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Total Groups Merged: {total_merged_groups}")
            print(f"Total Records Updated: {total_records_updated}")
        else:
            print("No auto-consolidations performed.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    consolidate_tier2_giants()
