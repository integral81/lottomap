
import json
import collections

# Load Data
try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except Exception as e:
    print(f"Error loading data: {e}")
    exit(1)

# Count wins per shop (Name + Address Key)
shop_wins = collections.defaultdict(int)
shop_details = {}

for item in data:
    # Normalize key: Remove spaces, keep core info
    name = item.get('n', '').strip()
    addr = item.get('a', '').strip()
    
    # Check for closed status in data
    is_closed = item.get('closed', False)
    
    key = f"{name}|{addr}"
    shop_wins[key] += 1
    
    # Store representative details (prefer not closed or latest)
    if key not in shop_details:
        shop_details[key] = {
            'n': name,
            'a': addr,
            'closed': is_closed,
            'wins': 0,
            'rounds': []
        }
    shop_details[key]['wins'] += 1
    shop_details[key]['rounds'].append(item.get('r'))
    if is_closed:
         shop_details[key]['closed'] = True # Mark if any record says closed (though usually it's per shop)

# Group by win count
counts = collections.defaultdict(list)
for key, info in shop_details.items():
    wins = info['wins']
    counts[wins].append(info)

# Output Results
print(f"Total Unique Shops: {len(shop_details)}")
print("-" * 30)
for w in sorted(counts.keys(), reverse=True):
    if w < 1: continue
    print(f"{w} Wins: {len(counts[w])} shops")

# Group all shops with 1-4 wins
shops_remaining = []
for w in [4, 3, 2, 1]:
    shops_remaining.extend(counts[w])

# Sort by wins desc, then name
shops_remaining.sort(key=lambda x: (-x['wins'], x['n']))

with open('shops_to_verify_all.json', 'w', encoding='utf-8') as f:
    json.dump(shops_remaining, f, ensure_ascii=False, indent=2)

print("-" * 30)
print(f"saved {len(shops_remaining)} shops with 1-4 wins to 'shops_to_verify_all.json'")
