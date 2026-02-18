import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def finalize_step13():
    print("--- [Step 13] Final DB Synchronization Started ---")
    
    # Setup Selenium (Headless for speed, or Headed to see)
    options = Options()
    # options.add_argument("--headless") # Let's keep it visible for the user to see the "Magic"
    options.add_argument("--start-maximized")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # 1. Connect to the running Pilot (Or open the file directly if server is down)
        # We assume the user has the pilot running on localhost:8000 from the batch file.
        # If not, we can access the file directly.
        pilot_url = "http://localhost:8000/pov_automation_pilot.html"
        print(f"Connecting to Pilot: {pilot_url}")
        driver.get(pilot_url)
        
        # 2. Wait for Step 13 (The result box to appear)
        print("Waiting for Pilot to complete calculation (Step 12 -> 13)...")
        MAX_WAIT = 60
        found_data = False
        
        pano_id = ""
        pan = 0.0
        
        for i in range(MAX_WAIT):
            try:
                # Check for the data box display
                data_box = driver.find_element(By.ID, "data-box-0")
                if data_box.is_displayed():
                    # Scrape values
                    pano_id = driver.find_element(By.ID, "pano-0").text
                    pan_text = driver.find_element(By.ID, "pan-0").text
                    
                    if pano_id != "-" and pan_text != "0":
                        pan = float(pan_text)
                        print(f"Captured Data -> PanoID: {pano_id}, Pan: {pan}")
                        found_data = True
                        break
            except:
                pass
            time.sleep(1)
            print(f"Processing... {i+1}/{MAX_WAIT}")
            
        if not found_data:
            print("[Error] Failed to capture data from Pilot. Is the Pilot running?")
            return

        # 3. Update lotto_data.json
        print("Updating Database...")
        db_path = "lotto_data.json"
        
        with open(db_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        updated = False
        for item in data:
            if item.get('n') == "현진식품":
                item['pov'] = {
                    "id": pano_id,
                    "pan": pan,
                    "tilt": 1.5, # Default from pilot
                    "zoom": 0 # Default
                }
                print(f"Updated [현진식품] with POV: {item['pov']}")
                updated = True
                break
                
        if updated:
            with open(db_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=0, separators=(',', ':'), ensure_ascii=False)
            print("[Success] Step 13 Complete: Database Updated!")
            
            # Create verification link
            create_verification_html(pano_id, pan)
            
        else:
            print("[Error] Could not find '현진식품' in database.")

    except Exception as e:
        print(f"[Error] {e}")
    finally:
        driver.quit()

def create_verification_html(pano_id, pan):
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>현진식품 POV 검증</title>
    <script type="text/javascript" src="https://dapi.kakao.com/v2/maps/sdk.js?appkey=84b62e85ed3ec32fca558717eda26006"></script>
    <style>
        body {{ margin:0; overflow:hidden; }}
        #roadview {{ width:100vw; height:100vh; }}
    </style>
</head>
<body>
    <div id="roadview"></div>
    <script>
        var rv = new kakao.maps.Roadview(document.getElementById('roadview'));
        var rc = new kakao.maps.RoadviewClient();
        rv.setPanoId({pano_id}, new kakao.maps.LatLng(0,0));
        kakao.maps.event.addListener(rv, 'init', function() {{
            rv.setViewpoint({{ pan: {pan}, tilt: 1.5, zoom: 0 }});
        }});
    </script>
</body>
</html>"""
    with open("verify_hyeonjin_final.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Created verify_hyeonjin_final.html")

if __name__ == "__main__":
    finalize_step13()
