
import json
import sys

def restore_pov():
    target_name = "로또휴게실"
    # User provided short address, but data has full address. We match by name.
    
    # User data:
    # { name: "로또휴게실", addr: "경기 용인시 기흥구", panoid: 1199447820, pov: { pan: 277.41, tilt: 2.00, "zoom": 1 } }
    
    new_pov = {
        "id": "1199447820", # Stringify just in case, though user gave int
        "pan": 277.41,
        "tilt": 2.00,
        "zoom": 1
    }
    
    json_path = 'lotto_data.json'
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        count = 0
        updated = False
        
        for item in data:
            if target_name in item['n']:
                # Update POV
                item['pov'] = new_pov
                count += 1
                updated = True
                
        if updated:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Successfully updated {count} records for '{target_name}' with restored POV.")
        else:
            print(f"Target '{target_name}' not found in data.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    restore_pov()
