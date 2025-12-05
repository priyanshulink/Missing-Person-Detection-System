@echo off
REM Camera Control Batch Script

if "%1"=="" goto usage
if "%1"=="list" goto list
if "%1"=="start" goto start
if "%1"=="stop" goto stop
if "%1"=="status" goto status
goto usage

:list
echo.
echo Listing all cameras...
python control_camera.py list
goto end

:start
if "%2"=="" (
    echo Error: Please specify camera ID
    echo Example: camera_control.bat start cam02
    goto end
)
echo.
echo Starting camera: %2
python control_camera.py start %2
goto end

:stop
if "%2"=="" (
    echo Error: Please specify camera ID
    echo Example: camera_control.bat stop cam02
    goto end
)
echo.
echo Stopping camera: %2
python control_camera.py stop %2
goto end

:status
if "%2"=="" (
    echo Error: Please specify camera ID
    echo Example: camera_control.bat status cam02
    goto end
)
echo.
echo Getting camera status: %2
python control_camera.py status %2
goto end

:usage
echo.
echo ========================================
echo   Camera Control System
echo ========================================
echo.
echo Usage:
echo   camera_control.bat list
echo   camera_control.bat start ^<camera_id^>
echo   camera_control.bat stop ^<camera_id^>
echo   camera_control.bat status ^<camera_id^>
echo.
echo Examples:
echo   camera_control.bat list
echo   camera_control.bat start cam02
echo   camera_control.bat stop cam02
echo   camera_control.bat status cam02
echo.
echo Camera IDs:
echo   cam02       - Library Hall Camera
echo   cam01       - Main Gate Camera
echo   cam_local   - Local Webcam
echo.

:end
