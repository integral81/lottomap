
import json

def check_overlap():
    try:
        with open('lotto_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        nara_1 = [] # Nam-bu-sun-hwan-ro
        nara_2 = [] # Euncheon-ro
        
        target_name = "복권나라"
        
        for entry in data:
            name = entry.get('n', '')
            addr = entry.get('a', '')
            round_num = entry.get('r', 0)
            
            if target_name in name:
                # Use partial match for address just in case
                if "남부순환로 1739-9" in addr:
                    nara_1.append(round_num)
                elif "은천로 40-1" in addr:
                    nara_2.append(round_num)
                    
        nara_1.sort()
        nara_2.sort()
        
        print(f"Location 1 (Nam-bu-sun-hwan-ro): {len(nara_1)} wins")
        print(f"Rounds: {nara_1}")
        
        print(f"Location 2 (Euncheon-ro): {len(nara_2)} wins")
        print(f"Rounds: {nara_2}")
        
        # Check overlap
        set1 = set(nara_1)
        set2 = set(nara_2)
        intersection = list(set1.intersection(set2))
        intersection.sort()
        
        if intersection:
            print(f"OVERLAP DETECTED: {intersection}")
        else:
            print("No overlap in rounds.")
            
        # Check ranges
        if nara_1:
            print(f"Range 1: {min(nara_1)} ~ {max(nara_1)}")
        if nara_2:
            print(f"Range 2: {min(nara_2)} ~ {max(nara_2)}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_overlap()
