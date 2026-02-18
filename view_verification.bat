@echo off
echo Starting Local Verification Server...
echo Please wait, the browser will open automatically.
echo (Do not close this window while viewing the map)
echo.

start "" "http://localhost:8000/verify_real_roadview.html"
python -m http.server 8000
pause
