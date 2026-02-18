
import json
from collections import Counter

def analyze_distribution():
    # We use audit_pov_stats.py's logic to group shops correctly
    try:
        with open('lotto_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error: {e}")
        return

    shops = {}
    for entry in data:
        if entry.get('n') == '인터넷 복권판매사이트' or entry.get('a') == '동행복권':
            continue
        key = (entry.get('n'), entry.get('a'))
        shops[key] = shops.get(key, 0) + 1

    counts = list(shops.values())
    dist = Counter(counts)
    
    # Sort by win count
    sorted_dist = sorted(dist.items())
    
    total_shops = len(shops)
    
    print("| 당첨 횟수 | 점포 수 | 비율 (%) | 누적 비율 (%) |")
    print("| :--- | :--- | :--- | :--- |")
    
    cumulative = 0
    for wins, count in sorted_dist:
        perc = (count / total_shops) * 100
        cumulative += count
        cum_perc = (cumulative / total_shops) * 100
        print(f"| {wins}회 | {count} | {perc:.2f}% | {cum_perc:.2f}% |")

    # Tiered Analysis Proposal Base
    print("\n--- Tiered Ranges ---")
    tiers = [
        (1, 2, "2회 이하"),
        (3, 4, "3~4회"),
        (5, 9, "5~9회"),
        (10, 100, "10회 이상")
    ]
    
    for start, end, label in tiers:
        t_count = sum(c for w, c in dist.items() if start <= w <= end)
        t_perc = (t_count / total_shops) * 100
        print(f"- {label}: {t_count}개 ({t_perc:.2f}%)")

if __name__ == "__main__":
    analyze_distribution()
