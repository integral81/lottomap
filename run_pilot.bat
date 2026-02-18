@echo off
echo Starting POV Automation Pilot System...
echo Target: Hyeonjin Food (Hyeonjin Sikpum)
echo.
echo Opening browser...
start "" "http://localhost:8000/pov_automation_pilot.html"
echo.
echo Server is running. Press Ctrl+C to stop.
python -m http.server 8000
pause
