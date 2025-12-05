@echo off
echo ========================================
echo   STOPPING ALL SERVICES
echo ========================================
echo.

echo Stopping Multi-Camera Surveillance...
taskkill /FI "WINDOWTITLE eq Multi-Camera Surveillance*" /F >nul 2>&1

echo Stopping Backend API...
taskkill /FI "WINDOWTITLE eq Backend API*" /F >nul 2>&1

echo Stopping Frontend...
taskkill /FI "WINDOWTITLE eq Frontend*" /F >nul 2>&1

echo Stopping Python processes...
taskkill /IM python.exe /F >nul 2>&1

echo Stopping Node processes...
taskkill /IM node.exe /F >nul 2>&1

echo.
echo ========================================
echo   ALL SERVICES STOPPED
echo ========================================
echo.
pause
