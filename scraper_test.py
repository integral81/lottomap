from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape_lotto_winners(start_round, end_round):
    """
    Simple sequential scraper (no threading)
    """
    chrome_options = Options()
    # Headless OFF for debugging
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver, 15)
    
    all_data = []
    
    try:
        url = "https://www.dhlottery.co.kr/wnprchsplcsrch/home"
        driver.get(url)
        print(f"Opened URL: {url}")
        time.sleep(2)  # Initial page load
        
        for round_num in range(start_round, end_round + 1):
            print(f"\n[{round_num}회차] Starting...")
            
            try:
                # Select round
                select_element = wait.until(EC.presence_of_element_located((By.ID, "srchLtEpsd")))
                select = Select(select_element)
                select.select_by_value(str(round_num))
                print(f"  - Selected round {round_num}")
                
                # Click search
                search_btn = driver.find_element(By.ID, "btnSrch")
                driver.execute_script("arguments[0].click();", search_btn)
                print(f"  - Clicked search button")
                
                # Wait for results
                time.sleep(2)
                
                # Extract data
                target_selector = "#storeDiv .store-box"
                try:
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, target_selector)))
                    boxes = driver.find_elements(By.CSS_SELECTOR, target_selector)
                    print(f"  - Found {len(boxes)} store boxes")
                except:
                    print(f"  - No data found (empty or loading failed)")
                    continue
                
                round_results = []
                for box in boxes:
                    try:
                        rank = box.find_element(By.CLASS_NAME, "draw-rank").text.strip()
                        if "1등" not in rank:
                            continue
                        
                        shop_name = box.find_element(By.CLASS_NAME, "store-loc").text.strip()
                        method = box.find_element(By.CLASS_NAME, "draw-opt").text.strip()
                        location = box.find_element(By.CLASS_NAME, "store-addr").text.strip()
                        
                        round_results.append({
                            "회차": round_num,
                            "등위": rank,
                            "상호명": shop_name,
                            "당첨방식": method,
                            "소재지": location
                        })
                    except Exception as e:
                        continue
                
                all_data.extend(round_results)
                print(f"  ✓ Collected {len(round_results)} records (Total: {len(all_data)})")
                
            except Exception as e:
                print(f"  ✗ Error: {e}")
                continue
        
    except Exception as e:
        print(f"\nFatal error: {e}")
    finally:
        driver.quit()
    
    # Save results
    if all_data:
        df = pd.DataFrame(all_data)
        df = df.sort_values(by="회차", ascending=False)
        output_file = "lotto_test_1_10.xlsx"
        df.to_excel(output_file, index=False)
        print(f"\n✓ Saved {len(df)} records to {output_file}")
    else:
        print("\n✗ No data collected")
    
    return len(all_data)

if __name__ == "__main__":
    print("=" * 60)
    print("Testing scraper with rounds 1-10")
    print("=" * 60)
    scrape_lotto_winners(1, 10)
