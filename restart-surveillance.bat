@echo off
echo ========================================
echo   RESTARTING SURVEILLANCE SYSTEM
echo ========================================
echo.

echo Stopping current surveillance...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq YOLO*" 2>nul

timeout /t 2 >nul

echo.
echo Starting surveillance with new settings...
cd ai-module
start "YOLO Surveillance" python yolo_integrated_surveillance.py

echo.
echo ========================================
echo   SURVEILLANCE RESTARTED
echo ========================================
echo.
echo The surveillance window should open.
echo Lower confidence threshold: 45%% (was 60%%)
echo.
pause
