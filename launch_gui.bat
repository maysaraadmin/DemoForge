@echo off
echo Starting DemoForge GUI Manager with Embedded Browser...
echo.
echo Features:
echo - Real-time Docker Compose monitoring
echo - Embedded web browser for service access
echo - Service logs viewer
echo - Individual service control
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "gui_manager.py" (
    echo Error: gui_manager.py not found in current directory
    echo Please run this batch file from the DemoForge directory
    pause
    exit /b 1
)

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo Warning: Docker Desktop may not be running
    echo Please start Docker Desktop and try again
    echo.
    pause
)

echo Launching GUI...
python launch_gui.py

if errorlevel 1 (
    echo.
    echo Error: Failed to start GUI
    echo Make sure you have installed the required dependencies:
    echo pip install -r requirements.txt
    echo.
    echo Note: PyQt5-WebEngine requires Visual C++ Build Tools on Windows
    echo.
    pause
)
