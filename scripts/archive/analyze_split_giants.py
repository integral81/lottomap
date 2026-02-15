import json

def analyze_split_giants():
    json_path = 'lotto_data.json'
    target_keywords = ["스파", "부일카", "인주", "세진전자", "로또휴게실"]
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        for keyword in target_keywords:
            print(f"\n--- Analysis for '{keyword}' ---")
            variants = {}
            for item in data:
                if keyword in item.get('n', ''):
                    addr = item.get('a', 'Unknown')
                    if addr not in variants:
                        variants[addr] = 0
                    variants[addr] += 1
            
            for addr, count in variants.items():
                print(f"  {addr}: {count} wins")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze_split_giants()
