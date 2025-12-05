@echo off
echo ========================================
echo Person Detection System - Startup Script
echo ========================================
echo.

REM Check if MongoDB is running
echo [1/4] Checking MongoDB...
sc query MongoDB | find "RUNNING" >nul
if errorlevel 1 (
    echo MongoDB is not running. Starting MongoDB...
    net start MongoDB
) else (
    echo MongoDB is already running.
)
echo.

REM Start Backend API
echo [2/4] Starting Backend API...
start "Backend API" cmd /k "cd /d %~dp0..\backend-api && npm start"
timeout /t 5 /nobreak >nul
echo.

REM Start AI Module
echo [3/4] Starting AI Module...
start "AI Module" cmd /k "cd /d %~dp0..\ai-module && python main.py"
timeout /t 3 /nobreak >nul
echo.

REM Open Dashboard
echo [4/4] Opening Dashboard...
timeout /t 2 /nobreak >nul
start "" "%~dp0..\frontend\index.html"
echo.

echo ========================================
echo System Started Successfully!
echo ========================================
echo.
echo Backend API: http://localhost:3000
echo Dashboard: Check your browser
echo.
echo Press any key to exit this window...
pause >nul
