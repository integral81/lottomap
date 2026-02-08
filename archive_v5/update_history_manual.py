import json
import os

HISTORY_FILE = 'lotto_history.json'

def update_history():
    if not os.path.exists(HISTORY_FILE):
        print("History file not found!")
        return

    with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Data from search result
    fixes = {
        "480": [3, 5, 10, 17, 30, 31],
        "481": [3, 4, 23, 29, 40, 41],
        "482": [10, 16, 24, 25, 35, 43],
        "483": [12, 15, 19, 22, 28, 34],
        "484": [1, 3, 27, 28, 32, 45],
        "485": [17, 22, 26, 27, 36, 39],
        "486": [1, 2, 23, 25, 38, 40],
        "487": [4, 8, 25, 27, 37, 41],
        "488": [2, 8, 17, 30, 31, 38],
        "489": [2, 4, 8, 15, 20, 27],
        "490": [1, 13, 22, 23, 30, 31],
        "491": [8, 17, 35, 36, 39, 42],
        "492": [22, 27, 31, 35, 37, 40],
        "493": [20, 22, 26, 33, 36, 37],
        "494": [12, 14, 18, 21, 31, 34],
        "495": [4, 13, 22, 27, 34, 44],
        "496": [4, 13, 20, 29, 36, 41],
        "497": [19, 20, 23, 24, 43, 44]
    }

    for k, v in fixes.items():
        v.sort()
        data[k] = v
        print(f"Updated {k}: {v}")

    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False) # Compact

    print("Manual update complete.")

if __name__ == "__main__":
    update_history()
