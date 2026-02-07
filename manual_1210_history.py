from auto_update import scrape_winning_numbers, update_historic_file
import pandas as pd

def check_file(filename):
    try:
        df = pd.read_excel(filename)
        print(f"Latest round in {filename}: {df['회차'].max()}")
        if 1210 in df['회차'].values:
            print("Round 1210 is present.")
            print(df[df['회차'] == 1210])
        else:
            print("Round 1210 is NOT present.")
    except Exception as e:
        print(f"Error reading file: {e}")

if __name__ == "__main__":
    print("--- BEFORE UPDATE ---")
    check_file("lotto_historic_numbers_1_1209_Final.xlsx")
    
    print("\n--- UPDATING ---")
    nums = [1, 7, 9, 17, 27, 38] # Hardcoded from search results
    if nums:
        print(f"Scraped numbers: {nums}")
        update_historic_file(1210, nums)
    else:
        print("Failed to scrape numbers.")
        
    print("\n--- AFTER UPDATE ---")
    check_file("lotto_historic_numbers_1_1209_Final.xlsx")
