@echo off
echo ========================================
echo   STARTING SURVEILLANCE SYSTEM
echo ========================================
echo.
echo Make sure you have added cameras first!
echo.
echo Starting Multi-Camera Surveillance...
start "Multi-Camera Surveillance" cmd /k "cd ai-module && python multi_camera_surveillance.py"
timeout /t 3 >nul
echo.
echo ========================================
echo   SURVEILLANCE STARTED
echo ========================================
echo.
echo Check the "Multi-Camera Surveillance" window for status.
echo.
pause
