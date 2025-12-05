@echo off
echo ========================================
echo   FIRST TIME SETUP
echo ========================================
echo.
echo This will:
echo 1. Check MongoDB is running
echo 2. Seed cameras to database
echo 3. Start all services
echo.
echo Press any key to continue...
pause >nul

echo.
echo [1/3] Checking MongoDB...
sc query MongoDB | find "RUNNING" >nul
if %errorlevel% equ 0 (
    echo     ✅ MongoDB is running
) else (
    echo     Starting MongoDB...
    net start MongoDB
    timeout /t 3 >nul
)
echo.

echo [2/3] Seeding cameras to database...
cd backend-api
node seed-cameras.js
cd ..
echo.

echo [3/3] Starting all services...
timeout /t 2 >nul
call start_all.bat
