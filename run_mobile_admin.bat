@echo off
echo ==================================================
echo 📱 Starting Mobile Admin Console
echo ==================================================
echo.
echo [1] Finding your Local IP Address...
echo --------------------------------------------------
ipconfig | findstr "IPv4"
echo --------------------------------------------------
echo.
echo [2] Launching Server...
echo Please access the following URL from your mobile phone:
echo http://[YOUR-IP-ABOVE]:8000/mobile_admin.html
echo.
echo Example: http://192.168.0.5:8000/mobile_admin.html
echo.
echo (Press Ctrl+C to stop)
python admin_server.py
pause
