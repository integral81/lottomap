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

def test_scrape():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver, 10)
    
    try:
        url = "https://www.dhlottery.co.kr/wnprchsplcsrch/home"
        driver.get(url)
        time.sleep(2)
        
        # Check current round
        select_element = wait.until(EC.presence_of_element_located((By.ID, "srchLtEpsd")))
        select = Select(select_element)
        select.select_by_value("1209")
        
        search_btn = driver.find_element(By.ID, "btnSrch")
        driver.execute_script("arguments[0].click();", search_btn)
        time.sleep(1)
        
        boxes = driver.find_elements(By.CSS_SELECTOR, "#storeDiv .store-box")
        res = []
        for box in boxes:
            shop_name = box.find_element(By.CLASS_NAME, "store-loc").text.strip()
            location = box.find_element(By.CLASS_NAME, "store-addr").text.strip()
            print(f"Scraped: {shop_name} | {location}")
            res.append({"상호명": shop_name, "소재지": location})
        
        df = pd.DataFrame(res)
        df.to_excel("scrape_test_result.xlsx", index=False)
        print("Saved to scrape_test_result.xlsx")
        
        # Read it back and check
        df2 = pd.read_excel("scrape_test_result.xlsx")
        print("Read back first row:", df2.iloc[0].to_dict())
        
    finally:
        driver.quit()

if __name__ == "__main__":
    test_scrape()
