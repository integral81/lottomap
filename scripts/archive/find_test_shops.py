import json

with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 1-2회 당첨 점포 찾기
shops = [s for s in data if s.get('totalWins', 0) in [1, 2]][:3]

print("=== 테스트 점포 3개 (1-2회 당첨) ===\n")
for i, s in enumerate(shops, 1):
    print(f"{i}. {s['shopName']}")
    print(f"   주소: {s['address']}")
    print(f"   당첨: {s['totalWins']}회")
    print(f"   좌표: ({s['latitude']}, {s['longitude']})")
    print()
