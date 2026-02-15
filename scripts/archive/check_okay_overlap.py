
import json

def check_overlap_okay():
    try:
        with open('lotto_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        loc_1 = [] # 176
        loc_2 = [] # 19-3
        
        target_name = "오케이상사"
        
        for entry in data:
            name = entry.get('n', '')
            addr = entry.get('a', '')
            round_num = entry.get('r', 0)
            
            if target_name in name:
                if "176" in addr:
                    loc_1.append(round_num)
                elif "19-3" in addr:
                    loc_2.append(round_num)
                    
        loc_1.sort()
        loc_2.sort()
        
        print(f"Okay Sangsa 1 (176): {len(loc_1)} wins")
        print(f"Rounds: {loc_1}")
        
        print(f"Okay Sangsa 2 (19-3): {len(loc_2)} wins")
        print(f"Rounds: {loc_2}")
        
        # Check overlap
        set1 = set(loc_1)
        set2 = set(loc_2)
        intersection = list(set1.intersection(set2))
        intersection.sort()
        
        if intersection:
            print(f"OVERLAP DETECTED: {intersection}")
        else:
            print("No overlap in rounds.")
            
        if loc_1: print(f"Range 1: {min(loc_1)} ~ {max(loc_1)}")
        if loc_2: print(f"Range 2: {min(loc_2)} ~ {max(loc_2)}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_overlap_okay()
