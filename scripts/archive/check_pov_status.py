import json

def check_registration(shop_names):
    json_path = 'lotto_data.json'
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        for shop_name in shop_names:
            results = [item for item in data if shop_name in item.get('n', '')]
            print(f"\n--- {shop_name} ---")
            print(f"Found {len(results)} records.")
            unregistered = [r for r in results if 'pov' not in r]
            print(f"Unregistered (missing pov): {len(unregistered)}")
            if results:
                print("Sample POC data from first record:", results[0].get('pov', 'N/A'))
                
    except Exception as e:
        print(f"Error reading lotto_data.json: {e}")

if __name__ == "__main__":
    check_registration(["부자랑", "북부슈퍼"])
