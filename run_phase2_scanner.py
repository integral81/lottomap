import os
import threading
import time
import subprocess
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler

def run_server():
    print("Starting Local Server on port 8000...")
    os.chdir(r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map")
    httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
    httpd.serve_forever()

def launch_secure_browser():
    # Path to Chrome (Assuming standard install on Windows)
    # We try typical paths
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Users\%USERNAME%\AppData\Local\Google\Chrome\Application\chrome.exe"
    ]
    
    chrome_exe = None
    for path in chrome_paths:
        expanded = os.path.expandvars(path)
        if os.path.exists(expanded):
            chrome_exe = expanded
            break
            
    if not chrome_exe:
        print("Could not find Chrome executable.")
        return

    print(f"Found Chrome: {chrome_exe}")
    
    # URL to open
    url = "http://localhost:8000/pov_phase2_pilot.html"
    
    # Args for disabling security (Required for Canvas Taint / CORS)
    user_data_dir = os.path.abspath("chrome_dev_profile")
    if not os.path.exists(user_data_dir):
        os.makedirs(user_data_dir)
        
    cmd = [
        chrome_exe,
        "--user-data-dir=" + user_data_dir,
        "--disable-web-security", # The magic flag
        "--disable-site-isolation-trials",
        "--new-window",
        url
    ]
    
    print("Launching Chrome with --disable-web-security...")
    subprocess.Popen(cmd)

if __name__ == "__main__":
    # 1. Start Server in background thread
    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    
    # 2. Wait a bit for server
    time.sleep(2)
    
    # 3. Launch Browser
    launch_secure_browser()
    
    print("\nScanner is running!")
    print("Keep this window open while the scanner works.")
    print("Press Ctrl+C to stop the server.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")
