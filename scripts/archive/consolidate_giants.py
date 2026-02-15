import json

def consolidate_giants():
    json_path = 'lotto_data.json'
    
    # 1. Define Master Data for Giants
    # These are the "Canonical" states we want everything to merge INTO.
    # I obtained POVs from previous context or will use existing ones if available.
    # Actually, I should find the record that HAS the POV and use that as base, 
    # OR if none have POV, I might need to find it (but most giants likely have it in at least one record).
    
    # Let's simple-merge by name/region first, ensuring we keep the best address and POV.
    
    consolidation_rules = [
        {
            "name": "스파",
            "matches": ["노원", "상계"], # Match '스파' in '노원' or '상계'
            "master_addr": "서울 노원구 동일로 1493 (상계동 666-3 주공10단지종합상가111)",
            "master_pov": {"id": "1182675681", "pan": 154.6, "tilt": -3.5, "zoom": 0} # Example POV, will verify if exists in data
        },
        {
            "name": "부일카서비스",
            "matches": ["부산", "범일", "자성로"],
            "master_addr": "부산 동구 자성로133번길 35 (범일동 830-195)",
            "master_pov": {"id": "1202353723", "pan": 139.6, "tilt": 8.1, "zoom": 0}
        },
        {
            "name": "로또명당인주점",
            "matches": ["아산", "인주", "서해로"],
            "master_addr": "충남 아산시 인주면 서해로 519-2",
            "master_pov": {"id": "1198421051", "pan": 242.4, "tilt": 5.8, "zoom": 0} # Need to verify POV ID
        },
        {
            "name": "세진전자통신",
            "matches": ["대구", "서구", "평리", "서대구로"],
            "master_addr": "대구 서구 서대구로 376 (평리동 1094-4)",
            "master_pov": None # Will find from existing data
        },
        {
            "name": "로또휴게실",
            "matches": ["용인", "기흥", "용구대로", "상갈"],
            "master_addr": "경기 용인시 기흥구 용구대로 1885 (보라동 378-1)",
            "master_pov": None 
        }
    ]
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Helper to find existing POV if master doesn't have one
        def find_best_pov(records):
            for r in records:
                if "pov" in r and r["pov"]:
                    return r["pov"]
            return None

        total_updates = 0
        
        for rule in consolidation_rules:
            print(f"Consolidating {rule['name']}...")
            
            target_records = []
            for item in data:
                if rule['name'] in item['n']:
                    # Check region match
                    if any(m in item['a'] for m in rule['matches']):
                        target_records.append(item)
            
            if not target_records:
                continue
                
            # Determine master POV
            final_pov = rule['master_pov']
            if not final_pov:
                final_pov = find_best_pov(target_records)
                
            # Apply to all
            for item in target_records:
                item['n'] = rule['name']
                item['a'] = rule['master_addr']
                # Use coordinates of the one that had POV, or don't update lat/lng if we trust them?
                # Better to unify lat/lng too.
                # Let's find a record with lat/lng and use it as master coords
                
                # Check if this item is the source of POV/Coords
                # Actually, let's just pick the latest address one or the one with POV
                pass # Just grouping for now
            
            # Real update:
            # We want to enable the POV for ALL of them.
            # And standardise address.
            
            count = 0
            for item in target_records:
                item['n'] = rule['name']
                item['a'] = rule['master_addr']
                if final_pov:
                    item['pov'] = final_pov
                # Update coods if available in rule or leave as is? 
                # Ideally they should all be same.
                # Let's take coords from the "best" record
                best_record = next((r for r in target_records if 'pov' in r and r['pov']), target_records[0])
                item['lat'] = best_record['lat']
                item['lng'] = best_record['lng']
                
                if 'closed' in item:
                    del item['closed']
                count += 1
            
            print(f"  -> Merged {count} records.")
            total_updates += count

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"Total consolidated: {total_updates}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    consolidate_giants()
