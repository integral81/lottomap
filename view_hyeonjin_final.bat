@echo off
echo Starting Local Verification Server for Hyeonjin Food...
echo The browser will open automatically.
echo (Do not close this window while viewing the map)
echo.

start "" "http://localhost:8000/verify_hyeonjin_final.html"
python -m http.server 8000
pause
