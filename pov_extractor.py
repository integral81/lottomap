import sys
import io

# 한글 출력 깨짐 방지
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

def human_type(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.15))

def check_rv_active(driver):
    try:
        if "roadview" in driver.current_url or "pano" in driver.current_url:
            return True
        # 로드뷰 전용 버튼들 탐색
        driver.find_element(By.CSS_SELECTOR, "button[data-id='openUtilBtn'], .btn_set")
        return True
    except:
        return False

def extract_pov(target_name, target_addr):
    print(f"--- [{target_name}] POV 추출 프로세스 시작 ---", flush=True)
    
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_experimental_option("detach", True)
    # 자동화 배너 및 제어 흔적 제거
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    # 실제 브라우저처럼 보이게 하기 위한 User-Agent 설정
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # navigator.webdriver 속성 제거 (탐지 우회 핵심)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    })
    
    wait = WebDriverWait(driver, 20)
    actions = ActionChains(driver)

    try:
        driver.get("https://map.kakao.com")
        time.sleep(3)

        # 검색어 입력
        print("검색어 입력 중...", flush=True)
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "search.keyword.query")))
        human_type(search_box, target_addr)
        time.sleep(1)

        # 검색 버튼 클릭 (엔터 키 입력 시뮬레이션으로 우회)
        print("검색 실행 (Enter 입력)...", flush=True)
        search_box.send_keys(Keys.ENTER)
        
        # 검색 결과 대기 (첫 번째 장소)
        print("검색 결과 수신 대기 중...", flush=True)
        # .PlaceItem 클래스는 개별 검색 결과 항목을 의미함
        first_place = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".PlaceItem:nth-child(1), li.PlaceItem")))
        
        # 장소 이름 확인
        place_name = first_place.find_element(By.CSS_SELECTOR, ".tit_name, .link_name").text
        print(f"식별된 장소: {place_name}", flush=True)

        target_found = first_place # 기본값

        # [스마트 검색 알고리즘] 정확도 기반 매칭
        print("검색 결과 분석 중... (이름+주소 매칭 알고리즘 가동)", flush=True)
        items = driver.find_elements(By.CSS_SELECTOR, ".PlaceItem, li.PlaceItem")
        
        for item in items:
            try:
                p_name = item.find_element(By.CSS_SELECTOR, ".tit_name, .link_name").text
                p_addr = item.find_element(By.CSS_SELECTOR, ".addr").text
                print(f"   - 후보: {p_name} / {p_addr}", flush=True)
                
                # "현진식품" & "중앙로 32" (주소의 일부) 매칭 확인
                if "현진식품" in p_name and ("중앙로 32" in p_addr or "구로구" in p_addr):
                    target_found = item
                    print(f"   >> [일치!] 타겟을 확인했습니다: {p_name}", flush=True)
                    break
            except: pass

        # [Step 1] 검색 완료 후 일시정지 (사용자 확인)
        print(f"\n>> [Step 1 완료] '{target_name}' 검색 및 매칭 완료.", flush=True)
        print(">> 브라우저에서 장소(현진식품)가 맞는지 확인하세요.", flush=True)
        print(">> 확인되셨으면 엔터(Enter)를 입력하여 로드뷰 진입 단계로 넘어갑니다...", flush=True)
        input() 

        # 로드뷰 활성화 시도
        print("\n" + "🚀"*30, flush=True)
        print(f" [Step 2 시작] '{target_name}'의 로드뷰 버튼(노란 세모)을 클릭합니다!", flush=True)
        print("🚀"*30, flush=True)
        
        # 만약 이미 로드뷰 상태라면 바로 점프!
        if check_rv_active(driver):
            print("\n>> [와우!] 벌써 가게 앞에 도착해 계시네요!", flush=True)
        else:
            try:
                # 타겟 아이템 내부의 로드뷰 버튼 찾기
                rv_btn = target_found.find_element(By.CSS_SELECTOR, "a.roadview, .btn_roadview, .ico_roadview")
                driver.execute_script("arguments[0].click();", rv_btn)
                print(">> [클릭] 리스트 매칭 기반으로 정확한 로드뷰 버튼을 눌렀습니다.", flush=True)
            except:
                print(">> [재시도] 리스트 버튼 실패, 일반 진입을 시도합니다.", flush=True)

            # 로드뷰 로딩 대기
            while not check_rv_active(driver):
                time.sleep(1)
            print("\n>> [진입 성공] 로드뷰 화면이 켜졌습니다.", flush=True)

        # [Step 2 완료] 로드뷰 진입 후 일시정지 (각도 조절)
        print("\n" + "👁️"*30, flush=True)
        print(" [Step 2 완료] 로드뷰 진입 성공.", flush=True)
        print(" >> 이제 화면상의 '현진식품' 정면 각도를 맞춰주세요.", flush=True)
        print(" >> 각도가 준비되면 엔터(Enter)를 입력하세요. 즉시 링크를 따겠습니다!", flush=True)
        print("👁️"*30, flush=True)
        input()

        # [Step 3] 공유 및 추출 (초고속 안정형)
        print("\n" + "⚡"*30, flush=True)
        print(" [Step 3 시작] 공유 버튼 클릭 및 링크 추출", flush=True)
        print("⚡"*30, flush=True)

        try:
            # 1. 메뉴(...) 버튼 클릭 (즉시 실행)
            try:
                util_box = driver.find_element(By.CSS_SELECTOR, "div.box_util")
                if "util_on" not in util_box.get_attribute("class"):
                    util_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn_set[data-id='openUtilBtn']")))
                    driver.execute_script("arguments[0].click();", util_btn)
                    print(">> [1/3] 메뉴 열기 완료", flush=True)
            except Exception as e:
                print(f">> [패스] 메뉴 열기 중 경미한 이슈: {e}", flush=True)

            # 2. 공유 버튼 클릭 (안정화 대기 1.5초)
            time.sleep(1.5) 
            share_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn_share[data-id='share']")))
            driver.execute_script("arguments[0].click();", share_btn)
            print(">> [2/3] 공유 버튼 클릭 완료 (안정적)", flush=True)

            # 3. 링크 추출 (팝업 뜨자마자 바로)
            link_el = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.btn_copyurl")))
            final_link = link_el.get_attribute("href")
            
            if final_link:
                print("\n" + "🎉"*30, flush=True)
                print(f" [미션 성공] URL 확보: {final_link}", flush=True)
                print("🎉"*30, flush=True)
                with open("extracted_url.txt", "w") as f:
                    f.write(final_link)
            else:
                print(">> [오류] 링크 요소가 비어있습니다.", flush=True)

        except Exception as e:
             print(f"\n>> [실패] 자동화 과정 중 오류 발생: {e}", flush=True)

        # 브라우저 유지
        print("\n모든 단계가 완료되었습니다. 브라우저는 10초 뒤에 정리할게요.", flush=True)
        while True:
            time.sleep(1)

    except Exception as e:
        print(f"시스템이 졸린가봐요: {e}")

if __name__ == "__main__":
    extract_pov("현진식품", "서울 구로구 중앙로 32")
