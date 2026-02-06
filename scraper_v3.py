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
from concurrent.futures import ThreadPoolExecutor
import threading

# Thread-safe list to collect data
all_data = []
data_lock = threading.Lock()

def normalize_text(text):
    if not isinstance(text, str): return text
    return import_unicodedata().normalize('NFC', text)

def import_unicodedata():
    import unicodedata
    return unicodedata

def scrape_batch(rounds):
    chrome_options = Options()
    # chrome_options.add_argument("--headless") # Headless off for debugging/anti-bot check
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Disable images and other resources for speed (maintain this)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver, 15) # Increased wait time
    
    try:
        url = "https://www.dhlottery.co.kr/wnprchsplcsrch/home"
        driver.get(url)
        
        for round_num in rounds:
            # print(f"[{round_num}회차] 수집 중...")
            try:
                # Select round
                try:
                    select_element = wait.until(EC.presence_of_element_located((By.ID, "srchLtEpsd")))
                    select = Select(select_element)
                    select.select_by_value(str(round_num))
                except:
                    print(f"[{round_num}회차] Select box fail, skipping...")
                    continue
                
                # Search
                try:
                    search_btn = driver.find_element(By.ID, "btnSrch")
                    driver.execute_script("arguments[0].click();", search_btn)
                except:
                    print(f"[{round_num}회차] Search button fail")
                    continue
                
                # Wait for loading
                time.sleep(1.0) # Increased delay for stability
                
                
                # Extract data
                target_selector = "#storeDiv .store-box"
                try:
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, target_selector)))
                    boxes = driver.find_elements(By.CSS_SELECTOR, target_selector)
                except:
                    print(f"[{round_num}회차] 데이터 없음 (Loading failed or Empty)")
                    continue
                
                batch_results = []
                for box in boxes:
                    try:
                        rank = box.find_element(By.CLASS_NAME, "draw-rank").text.strip()
                        if "1등" not in rank: continue
                        
                        shop_name = box.find_element(By.CLASS_NAME, "store-loc").text.strip()
                        method = box.find_element(By.CLASS_NAME, "draw-opt").text.strip()
                        location = box.find_element(By.CLASS_NAME, "store-addr").text.strip()
                        
                        batch_results.append({
                            "회차": round_num,
                            "등위": rank,
                            "상호명": normalize_text(shop_name),
                            "당첨방식": normalize_text(method),
                            "소재지": normalize_text(location)
                        })
                    except: continue
                
                with data_lock:
                    all_data.extend(batch_results)
                    print(f"[{round_num}회차] 수집 완료 ({len(batch_results)}건) - 누적 {len(all_data)}건")
                
            except Exception as e:
                print(f"[{round_num}회차] 치명적 에러: {e}")
                driver.get(url) # Refresh per error
                
    finally:
        driver.quit()

def main():
    start_round = 262  # 262회차가 1등 판매점 정보를 제공하는 첫 번째 회차
    end_round = 1209
    num_threads = 4 # Increased slightly for speed, assuming stable connection 
    
    rounds = list(range(start_round, end_round + 1))
    # Reverse order to get latest first (optional, but good for user feedback)
    rounds.reverse()
    
    chunk_size = (len(rounds) + num_threads - 1) // num_threads
    chunks = [rounds[i:i + chunk_size] for i in range(0, len(rounds), chunk_size)]
    
    print(f"Starting parallel scraping for {len(rounds)} rounds with {num_threads} threads...")
    print("This process will take some time. Please wait...")
    start_time = time.time()
    
    try:
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            executor.map(scrape_batch, chunks)
    except KeyboardInterrupt:
        print("\nScraping interrupted by user!")
    finally:
        # Save results even if interrupted
        if all_data:
            print("\nSaving collected data...")
            df = pd.DataFrame(all_data)
            df = df.sort_values(by="회차", ascending=False)
            output_file = "lotto_results_kinov_fresh.xlsx"
            df.to_excel(output_file, index=False)
            
            duration = time.time() - start_time
            print(f"Done! Saved {len(df)} records to {output_file}")
            print(f"Total time: {duration/60:.2f} minutes")
        else:
            print("No data collected.")

if __name__ == "__main__":
    main()
