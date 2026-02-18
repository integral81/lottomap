from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_verification_page():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless
    chrome_options.add_argument("--log-level=0") # Capture all logs
    
    # Enable browser logging
    d = webdriver.DesiredCapabilities.CHROME
    d['goog:loggingPrefs'] = { 'browser':'ALL' }

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        logger.info("Navigating to verification page on localhost...")
        driver.get("http://localhost:8000/verify_real_roadview.html")
        time.sleep(3) # Wait for load
        
        # Get browser logs
        logs = driver.get_log('browser')
        
        print("\n" + "="*50)
        print(" BROWSER CONSOLE LOGS ")
        print("="*50)
        
        has_error = False
        for entry in logs:
            if entry['level'] == 'SEVERE' or 'kakao' in entry['message']:
                print(f"[{entry['level']}] {entry['message']}")
                has_error = True
        
        if not has_error:
            print("No critical errors found in console.")
            
        print("="*50 + "\n")
        
        # Take screenshot to verify what selenium sees
        driver.save_screenshot("debug_verification_view.png")
        print("Screenshot saved to debug_verification_view.png")

    except Exception as e:
        logger.error(f"Error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    check_verification_page()
