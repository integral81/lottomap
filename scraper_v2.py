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
    chrome_options = Options()
    # chrome_options.add_argument("--headless") # 오류 디버깅을 위해 주석 처리 (창이 뜹니다)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.headless = False # 명시적 설정
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    all_data = []

    try:
        # 1. URL 수정 (사용자가 요청한 지도/리스트 형태 페이지)
        url = "https://www.dhlottery.co.kr/wnprchsplcsrch/home"
        driver.get(url)
        wait = WebDriverWait(driver, 15)

        for round_num in range(start_round, end_round + 1):
            print(f"[{round_num}회차] 수집 시작...")
            
            try:
                # 2. 회차 선택 (ID 수정: srchLtEpsd)
                # 간혹 페이지 로딩이 늦으면 요소를 못 찾을 수 있으므로 wait 사용
                select_element = wait.until(EC.presence_of_element_located((By.ID, "srchLtEpsd")))
                select = Select(select_element)
                select.select_by_value(str(round_num))
                
                # 3. 조회 버튼 클릭 (ID 수정: btnSrch)
                search_btn = driver.find_element(By.ID, "btnSrch")
                driver.execute_script("arguments[0].click();", search_btn) # JS 클릭으로 안정성 확보
                time.sleep(1)

                # 4. "1등" 탭 클릭 시도 (사용자가 강조한 노란색 영역)
                # 탭이 클릭되어야 1등 당첨점만 필터링되어 나옵니다.
                try:
                    # '1등' 텍스트를 포함하는 탭 요소를 찾아서 클릭
                    # 보통 탭은 ul > li > a 구조 또는 div > a 구조임
                    # XPath로 '1등' 텍스트가 있는 a 태그나 클릭 가능한 요소를 찾음
                    tab_xpath = "//*[contains(text(), '1등') and contains(@class, 'on')]" # 이미 활성화된 경우
                    
                    # 활성화가 안 되어 있다면 클릭해야 함
                    click_xpath = "//a[contains(text(), '1등')]"
                    try:
                        tab_btn = driver.find_element(By.XPATH, click_xpath)
                        tab_btn.click()
                        time.sleep(1) # 탭 전환 대기
                    except:
                        pass # 이미 1등 페이지이거나 찾을 수 없으면 진행
                except Exception:
                    pass

                # 5. 결과 로딩 대기
                # #storeDiv .store-box 구조
                target_selector = "#storeDiv .store-box"
                try:
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, target_selector)))
                    boxes = driver.find_elements(By.CSS_SELECTOR, target_selector)
                except:
                    print(f"   -> {round_num}회차 로딩 실패 또는 데이터 없음")
                    boxes = []
                
                # 6. 데이터 추출
                count = 0
                for box in boxes:
                    try:
                        # 상호명
                        shop_name = box.find_element(By.CLASS_NAME, "store-loc").text.strip()
                        
                        # 등위 (1등, 2등 등) - 없을 수도 있음 (예: 지역 헤더)
                        try:
                            rank_elem = box.find_element(By.CLASS_NAME, "draw-rank")
                            rank = rank_elem.text.strip()
                        except:
                            rank = ""
                        
                        # 1등만 수집 (사용자의 강조사항)
                        # rank 정보가 없거나 1등이 아니면 스킵
                        if "1등" not in rank:
                           continue

                        # 방법 (자동, 수동)
                        method = box.find_element(By.CLASS_NAME, "draw-opt").text.strip()
                        # 소재지
                        location = box.find_element(By.CLASS_NAME, "store-addr").text.strip()

                        data = {
                            "회차": round_num,
                            "등위": rank,
                            "상호명": shop_name,
                            "당첨방식": method,
                            "소재지": location
                        }
                        all_data.append(data)
                        count += 1
                    except Exception as e:
                        # print(f"    박스 파싱 중 오류: {e}")
                        continue
                
                print(f"   -> {count}개 점포 수집 완료")
                
            except Exception as e:
                print(f"   -> {round_num}회차 처리 중 오류: {e}")
                
            time.sleep(1)

    except Exception as e:
        print(f"전체 프로세스 오류 발생: {e}")
    finally:
        driver.quit()

    # 6. 결과 저장
    if all_data:
        df = pd.DataFrame(all_data)
        df.to_excel("lotto_results_kinov.xlsx", index=False)
        print(f"\n총 {len(all_data)}건 저장 완료: lotto_results_kinov.xlsx")
    else:
        print("데이터를 찾지 못했습니다.")

if __name__ == "__main__":
    scrape_lotto_winners(1207, 1209)
