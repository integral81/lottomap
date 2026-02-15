import json

def count_shops():
    json_path = 'lotto_data.json'
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        shops_with_pov = set()
        for item in data:
            if 'pov' in item:
                shops_with_pov.add(item.get('n'))
        
        print(f"Total Unique Shops with POV: {len(shops_with_pov)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    count_shops()
