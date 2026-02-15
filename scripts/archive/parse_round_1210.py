
from bs4 import BeautifulSoup
import json
import re

def parse_round_1210():
    try:
        with open('round_1210.html', 'r', encoding='utf-8') as f:
            html = f.read()
            
        soup = BeautifulSoup(html, 'html.parser')
        
        # 1st Prize Winners
        winners = []
        
        # Look for the table with class 'tbl_data'
        tables = soup.find_all('table', class_='tbl_data')
        
        # Typically the first table is 1st prize winners
        if not tables:
            print("No tables found")
            return

        rows = tables[0].find_all('tr')
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 5:
                continue
                
            # Column indices might vary, let's check
            # Usually: No, Shop Name, outcome(auto/manual), Address, etc.
            # Example: 1 | 상호명 | 자동 | 주소 | ...
            
            shop_name = cols[1].text.strip()
            method = cols[2].text.strip()
            address = cols[3].text.strip()
            
            # Clean up method (remove newlines/tabs)
            method = re.sub(r'\s+', '', method)
            
            # Clean up address (remove "지도보기" etc if present)
            # Sometimes address is in an 'a' tag or just text
            
            winner = {
                "r": 1210,
                "n": shop_name,
                "a": address,
                "m": method,
                "lat": None, # To be geocoded
                "lng": None
            }
            winners.append(winner)
            
        print(json.dumps(winners, ensure_ascii=False, indent=2))
        
        with open('round_1210_shops.json', 'w', encoding='utf-8') as f:
            json.dump(winners, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parse_round_1210()
