
import json

filepath = 'lotto_data.json'
with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

shop_a = "교통카드판매대"
shop_b = "고덕로또복권"

wins_a = []
wins_b = []

for item in data:
    if item['n'] == shop_a:
        wins_a.append(item['r'])
    if item['n'] == shop_b:
        wins_b.append(item['r'])

wins_a = sorted(list(set(wins_a)))
wins_b = sorted(list(set(wins_b)))

print(f"{shop_a} wins: {wins_a}")
print(f"{shop_b} wins: {wins_b}")

if wins_a and wins_b:
    print(f"{shop_a} last win: {wins_a[-1]}")
    print(f"{shop_b} first win: {wins_b[0]}")
