import json

with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Sort by totalWins (using totalWins calculated if available or inferring from rounds)
# Let's check the data structure again
# We saw ['n', 'm', 'a', 'r', 'lat', 'lng'] earlier. 
# Wait, I saw shop.totalWins in index.html, which means it might be calculated or present.

for s in data[:2]:
    print(s)

# Let's count occurrences of address/name to get totalWins if not present
from collections import Counter
counts = Counter(s['n'] + s['a'] for s in data)

shops_with_wins = []
seen = set()
for s in data:
    key = s['n'] + s['a']
    if key not in seen:
        s['totalWins'] = counts[key]
        shops_with_wins.append(s)
        seen.add(key)

# Top 5+ wins
top_shops = sorted([s for s in shops_with_wins if s['totalWins'] >= 10], key=lambda x: x['totalWins'], reverse=True)[:10]

print("\n=== 상위 당첨 점포 (10회 이상) ===")
for i, s in enumerate(top_shops, 1):
    print(f"{i}. {s['n']} | {s['a']} | {s['totalWins']}회")
