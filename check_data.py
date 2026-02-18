import json
import os

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        print(f"Total records: {len(data)}")
        if len(data) > 0:
            print(f"Sample record: {data[0]}")
            
        # Count wins
        from collections import Counter
        counts = Counter(item['n'] for item in data)
        three_wins = [k for k,v in counts.items() if v == 3]
        print(f"Shops with exactly 3 wins: {len(three_wins)}")
        print(f"Sample 3-win shops: {three_wins[:5]}")
        
except Exception as e:
    print(f"Error reading json: {e}")
