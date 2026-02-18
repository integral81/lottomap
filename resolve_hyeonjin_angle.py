import json
import math
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Constants
SHOP_NAME = "현진식품"
SHOP_LAT = 37.500768283874
SHOP_LNG = 126.863856941873
PANO_ID = 1198607745

def calculate_bearing(lat1, lng1, lat2, lng2):
    """
    Calculate initial bearing between two points.
    lat1, lng1: Start point (Pano)
    lat2, lng2: End point (Shop)
    """
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    diff_lng_rad = math.radians(lng2 - lng1)
    
    x = math.sin(diff_lng_rad) * math.cos(lat2_rad)
    y = math.cos(lat1_rad) * math.sin(lat2_rad) - math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(diff_lng_rad)
    
    initial_bearing = math.atan2(x, y)
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360
    return compass_bearing

def resolve_angle():
    print(f"Resolving Angle for {SHOP_NAME} (PanoID: {PANO_ID})...")
    
    # 1. Create a temporary HTML to fetch Pano Coordinates
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <body>
        <script type="text/javascript" src="https://dapi.kakao.com/v2/maps/sdk.js?appkey=84b62e85ed3ec32fca558717eda26006"></script>
        <div id="result"></div>
        <script>
            var rc = new kakao.maps.RoadviewClient();
            rc.getNearestPanoId(new kakao.maps.LatLng({SHOP_LAT}, {SHOP_LNG}), 50, function(panoId) {{
                // We assume the ID matches or is close enough. Let's find the location of THIS ID.
                // RoadviewClient doesn't directly give coords for an ID without loading raw data?
                // Actually `setPanoId` on a `Roadview` object allows getting position.
            }});
            
            // Allow fetching pano location by ID simulation
            // We use a dummy roadview to get the position
            document.write('<div id="rv" style="width:100px;height:100px;"></div>');
            var rv = new kakao.maps.Roadview(document.getElementById('rv'));
            rv.setPanoId({PANO_ID}, new kakao.maps.LatLng({SHOP_LAT}, {SHOP_LNG}));
            
            kakao.maps.event.addListener(rv, 'init', function() {{
                var pos = rv.getPosition();
                document.getElementById('result').innerText = pos.getLat() + "," + pos.getLng();
            }});
        </script>
    </body>
    </html>
    """
    
    with open("temp_resolve.html", "w", encoding="utf-8") as f:
        f.write(html_content)
        
    # 2. Use Selenium to get the coordinates
    options = Options()
    options.add_argument("--headless")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        import os
        url = "file://" + os.getcwd() + "/temp_resolve.html"
        driver.get(url)
        
        pano_lat = 0
        pano_lng = 0
        
        # Wait for result
        for i in range(10):
            try:
                res = driver.find_element(By.ID, "result").text
                if res:
                    parts = res.split(",")
                    pano_lat = float(parts[0])
                    pano_lng = float(parts[1])
                    break
            except:
                pass
            time.sleep(1)
            
        if pano_lat == 0:
            print("Failed to fetch Pano Coordinates.")
            return

        print(f"Pano Location: {pano_lat}, {pano_lng}")
        
        # 3. Calculate Bearing
        bearing = calculate_bearing(pano_lat, pano_lng, SHOP_LAT, SHOP_LNG)
        print(f"Calculated Bearing (Pan): {bearing:.2f}")
        
        # 4. Update JSON
        db_path = "lotto_data.json"
        
        with open(db_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        for item in data:
            if item.get('n') == SHOP_NAME:
                item['pov'] = {
                    "id": PANO_ID,
                    "pan": round(bearing, 1),
                    "tilt": 0, # Default
                    "zoom": 0
                }
                print(f"DB Updated: {item['pov']}")
                break
                
        with open(db_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=0, separators=(',', ':'), ensure_ascii=False)
            
        print("Success!")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    resolve_angle()
