@echo off
echo ============================================================
echo YOLOv8 Person Detection System - Installation
echo ============================================================
echo.

echo [1/3] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Error: Failed to create virtual environment
    echo Make sure Python 3.8+ is installed
    pause
    exit /b 1
)

echo [2/3] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/3] Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Installation Complete!
echo ============================================================
echo.
echo Next steps:
echo   1. Run: venv\Scripts\activate
echo   2. Test camera: python test_camera.py
echo   3. Add person: python add_person.py
echo   4. Run system: python main.py
echo.
echo See QUICKSTART.md for detailed instructions
echo.
pause
