
import json

def fix_dongtan_mismapping():
    file_path = 'lotto_data.json'
    print(f"--- [FIX] De-consolidating Dongtan (Gwangjang-ro 37) ---")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        dongtan_addr = "동탄중심상가2길 37 1층으"
        updated_count = 0
        
        # Mappings for mis-mapped rounds (from Excel ground truth)
        # Note: We need correct coordinates for these new addresses ideally, 
        # but for now, moving them to correct address strings is the priority for de-consolidation.
        # I will use a placeholder or trigger a re-geocoding flag.
        corrections = {
            1199: {"n": "신의한수", "a": "경기 화성시 떡전골로 86 103호"},
            1173: {"n": "강원세탁", "a": "경기 화성시 팔탄면 구장길 15-4"},
            1110: {"n": "매탄복권판매점", "a": "경기 화성시 영통로 59"},
            1066: {"n": "복권방", "a": "경기 화성시 병점3로 1"},
            929: {"n": "대박복권판매점", "a": "경기 화성시 남양읍 남양시장로 64"},
            914: {"n": "동탄 삼성 복권", "a": "경기 화성시 반송동 14-1 103호"},
            841: {"n": "복권명당", "a": "충북 진천군 진천읍 읍내리 202-7"} # Likely candidate for generic name
        }
        
        for item in data:
            addr = item.get('a', '').strip()
            round_num = item.get('r')
            
            # If it's the Dongtan address and in our correction list
            if addr == dongtan_addr and round_num in corrections:
                print(f"  Fixing Round {round_num}: {item['n']} -> {corrections[round_num]['n']}")
                item['n'] = corrections[round_num]['n']
                item['a'] = corrections[round_num]['a']
                # Reset lat/lng so they don't stay at Dongtan Gwangjang
                # Ideally we geocode them, but for now we null them to avoid false coordinates.
                item['lat'] = None
                item['lng'] = None
                item['relocated_verified'] = False
                updated_count += 1
            
            # Ensure the remaining 2 wins are named correctly
            elif addr == dongtan_addr and round_num in [704, 733]:
                if item['n'] != "광장복권판매점":
                    item['n'] = "광장복권판매점"
                    updated_count += 1

        if updated_count > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Successfully de-consolidated {updated_count} Dongtan entries.")
        else:
            print("No entries found to fix (already fixed or address mismatch).")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_dongtan_mismapping()
