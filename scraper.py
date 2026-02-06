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
    # Chrome 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Headless 모드 (화면을 보려면 이 라인을 주석 처리하세요)
    # chrome_options.add_argument("headless") # 일부 버전 호환성용
    # 디버깅 시 브라우저를 보려면 위 headless 설정을 주석 처리하고 아래 옵션을 사용하세요.
    # chrome_options.headless = False 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

    # WebDriver 초기화
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    all_data = []

    try:
        url = "https://dhlottery.co.kr/wnprchsplcsrch/home"
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        for round_num in range(start_round, end_round + 1):
            print(f"Collecting data for episode {round_num}...")
            
            try:
                # 첫 번째 회차 시도시 페이지 정보 출력 (디버깅용)
                if round_num == start_round:
                    print(f"  Current URL: {driver.current_url}")
                    print(f"  Title: {driver.title}")
                    selects = driver.find_elements(By.TAG_NAME, "select")
                    print(f"  Found {len(selects)} select elements. IDs: {[s.get_attribute('id') for s in selects]}")
                
                # 회차 선택 - id="drwNo"가 아니면 "srchDrwNo" 등을 찾아봄
                select_id = "drwNo"
                try:
                    select_element = wait.until(EC.presence_of_element_located((By.ID, select_id)))
                except:
                    print("  'drwNo' not found, trying 'srchDrwNo'...")
                    select_id = "srchDrwNo"
                    select_element = wait.until(EC.presence_of_element_located((By.ID, select_id)))
                select = Select(select_element)
                select.select_by_value(str(round_num))
                
                # 조회 버튼 클릭 (id="searchBtn")
                search_btn = wait.until(EC.element_to_be_clickable((By.ID, "searchBtn")))
                search_btn.click()
                
                # 결과 리스트 로딩 대기 (최대 10초)
                # 새로운 구조: #storeDiv 내부의 .store-box 요소들
                try:
                    target_selector = "#storeDiv .store-box"
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, target_selector)))
                    
                    # 로딩 후 잠시 안정화
                    time.sleep(1) 
                    
                    # 데이터 추출
                    boxes = driver.find_elements(By.CSS_SELECTOR, target_selector)
                    
                    # 디버깅: 페이지 로드 확인
                    print(f"  Load complete. Found {len(boxes)} shops. Title: {driver.title}")

                except Exception as e:
                    print(f"  Timeout or error waiting for store list: {e}")
                    boxes = []
                
                # 데이터가 없는 경우 처리
                if not boxes:
                    print(f"No data found for episode {round_num}")
                    continue
                
                count = 0
                for box in boxes:
                    try:
                        # 상호명: .store-loc
                        shop_name_elem = box.find_element(By.CLASS_NAME, "store-loc")
                        shop_name = shop_name_elem.text.strip()
                        
                        # 당첨등위: .draw-rank (예: 1등)
                        rank_elem = box.find_element(By.CLASS_NAME, "draw-rank")
                        rank = rank_elem.text.strip()

                        # 당첨방식: .draw-opt (예: 자동, 수동)
                        method_elem = box.find_element(By.CLASS_NAME, "draw-opt")
                        winning_method = method_elem.text.strip()
                        
                        # 소재지: .store-addr
                        addr_elem = box.find_element(By.CLASS_NAME, "store-addr")
                        location = addr_elem.text.strip()

                        # 1등 당첨점만 수집하려면 아래 주석 해제하여 필터링 가능
                        # if "1등" not in rank:
                        #     continue

                        all_data.append({
                            "회차": round_num,
                            "등위": rank,
                            "상호명": shop_name,
                            "당첨방식": winning_method,
                            "소재지": location
                        })
                        count += 1
                    except Exception as e:
                        print(f"    Error parsing a box: {e}")
                        continue
                
                print(f"  -> Extracted {count} shops.")
                
            except Exception as e:
                print(f"  -> Failed to collect episode {round_num}: {e}")
            
            time.sleep(1)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

    # 결과 저장
    if all_data:
        df = pd.DataFrame(all_data)
        df.to_excel("lotto_data.xlsx", index=False)
        print(f"Successfully saved {len(all_data)} records to lotto_data.xlsx")
    else:
        print("No data collected.")

if __name__ == "__main__":
    scrape_lotto_winners(1207, 1209)
