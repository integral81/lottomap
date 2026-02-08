import json
import requests
import time
import random
import os
from bs4 import BeautifulSoup

HISTORY_FILE = 'lotto_history.json'
MAX_ROUND = 1210

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return {}
    with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except:
            return {}

def save_history(data):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

def scrape_round(round_no):
    url = f"https://dhlottery.co.kr/gameResult.do?method=byWin&drwNo={round_no}"
    print(f"Scraping round {round_no}...")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        
        soup = BeautifulSoup(resp.content, 'html.parser')
        
        win_result_div = soup.find('div', class_='win_result')
        if not win_result_div:
            return None
            
        main_nums_div = win_result_div.find('div', class_='num win')
        if not main_nums_div:
            return None
            
        main_spans = main_nums_div.find_all('span', class_='ball_645')
        main_numbers = [int(s.text) for s in main_spans]
        
        if len(main_numbers) == 6:
            main_numbers.sort()
            return main_numbers
        return None

    except Exception as e:
        print(f"Error scraping round {round_no}: {e}")
        return None

def main():
    data = load_history()
    missing_rounds = []
    
    print(f"Auditing rounds 1 to {MAX_ROUND}...")
    for r in range(1, MAX_ROUND + 1):
        sr = str(r)
        if sr not in data:
            missing_rounds.append(r)
        else:
            entry = data[sr]
            if not isinstance(entry, list) or len(entry) != 6:
                print(f"Invalid data for round {r}: {entry}")
                missing_rounds.append(r)
    
    print(f"Found {len(missing_rounds)} missing/invalid rounds.")
    missing_rounds.sort()
    
    for round_no in missing_rounds:
        vals = scrape_round(round_no)
        if vals:
            data[str(round_no)] = vals
            print(f"Fixed round {round_no}: {vals}")
            save_history(data)
            time.sleep(random.uniform(1.0, 2.0))
        else:
            print(f"Failed to fix round {round_no}")
    
    print("Audit complete.")

if __name__ == "__main__":
    main()
