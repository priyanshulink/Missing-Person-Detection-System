@echo off
echo ========================================
echo   PERSON DETECTION SYSTEM - STARTUP
echo ========================================
echo.
echo Starting all services...
echo.

REM Check if MongoDB is running
echo [1/4] Checking MongoDB...
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
echo [2/4] Starting Backend API Server...
start "Backend API" cmd /k "cd backend-api && echo Starting Backend API... && node server.js"
timeout /t 5 >nul
echo     Backend API started on http://localhost:3000
echo.

REM Start Frontend
echo [3/4] Starting Frontend Server...
start "Frontend" cmd /k "cd frontend && echo Starting Frontend... && python -m http.server 8080"
timeout /t 3 >nul
echo     Frontend started on http://localhost:8080
echo.

REM Wait for backend to be ready
echo [4/5] Waiting for backend to be ready...
timeout /t 3 >nul
echo.

REM Start Multi-Camera Surveillance
echo [5/5] Starting Multi-Camera Surveillance System...
start "Multi-Camera Surveillance" cmd /k "cd ai-module && echo Starting Multi-Camera Surveillance... && python multi_camera_surveillance.py"
timeout /t 3 >nul
echo     Multi-Camera Surveillance started
echo.

echo ========================================
echo   ALL SERVICES STARTED SUCCESSFULLY!
echo ========================================
echo.
echo Services Running:
echo   - MongoDB:        Running
echo   - Backend API:    http://localhost:3000
echo   - Frontend:       http://localhost:8080
echo   - Surveillance:   Multi-Camera System Active
echo.
echo ========================================
echo   NEXT STEPS
echo ========================================
echo.
echo 1. Open browser: http://localhost:8080
echo 2. Login with:
echo    Username: ompriyanshu12@gmail.com
echo    Password: pradeep3133
echo 3. All active cameras are now streaming!
echo 4. Check "Multi-Camera Surveillance" window for camera status
echo.
echo Active Cameras:
echo   - Library Hall Camera (cam02): http://10.28.71.10:8080/video
echo   - Local Webcam (cam_local): Default webcam
echo.
echo ========================================
echo.
echo Press any key to open dashboard in browser...
pause >nul

start http://localhost:8080

echo.
echo Dashboard opened in browser!
echo.
echo To stop all services, close all command windows.
echo.
pause
