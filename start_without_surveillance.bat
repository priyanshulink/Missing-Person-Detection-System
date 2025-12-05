@echo off
echo ========================================
echo   STARTING BACKEND AND FRONTEND ONLY
echo   (Without Surveillance)
echo ========================================
echo.

REM Check if MongoDB is running
echo [1/3] Checking MongoDB...
sc query MongoDB | find "RUNNING" >nul
if %errorlevel% equ 0 (
    echo     MongoDB is running
) else (
    echo     Starting MongoDB...
    net start MongoDB
    timeout /t 3 >nul
)
echo.

REM Start Backend API
echo [2/3] Starting Backend API Server...
start "Backend API" cmd /k "cd backend-api && echo Starting Backend API... && node server.js"
timeout /t 5 >nul
echo     Backend API started on http://localhost:3000
echo.

REM Start Frontend
echo [3/3] Starting Frontend Server...
start "Frontend" cmd /k "cd frontend && echo Starting Frontend... && python -m http.server 8080"
timeout /t 3 >nul
echo     Frontend started on http://localhost:8080
echo.

echo ========================================
echo   BACKEND AND FRONTEND STARTED
echo ========================================
echo.
echo Services Running:
echo   - MongoDB:        Running
echo   - Backend API:    http://localhost:3000
echo   - Frontend:       http://localhost:8080
echo.
echo ========================================
echo   NEXT STEPS
echo ========================================
echo.
echo 1. Open browser: http://localhost:8080
echo 2. Login and add your cameras
echo 3. Then run: start_surveillance_only.bat
echo.
echo Press any key to open dashboard...
pause >nul

start http://localhost:8080

echo.
echo Dashboard opened!
echo.
echo After adding cameras, run:
echo   start_surveillance_only.bat
echo.
pause
