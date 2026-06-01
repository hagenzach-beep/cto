@echo off
REM PowerScale CTO JSON Generator - Windows Startup Script
REM This script sets up and runs the Flask application

echo ==============================================
echo PowerScale CTO JSON Generator
echo ==============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    python3 --version >nul 2>&1
    if errorlevel 1 (
        echo ERROR: Python is not installed. Please install Python 3.8 or higher.
        echo Download from: https://www.python.org/downloads/
        pause
        exit /b 1
    ) else (
        set PYTHON_CMD=python3
    )
) else (
    set PYTHON_CMD=python
)

echo Using Python: %PYTHON_CMD%

REM Check if virtual environment exists, if not create it
if not exist "venv" (
    echo Creating virtual environment...
    %PYTHON_CMD% -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo.
echo ==============================================
echo Starting PowerScale CTO JSON Generator...
echo Access the application at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo ==============================================
echo.

REM Run the application
flask run --host=0.0.0.0 --port=5000

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo An error occurred. Press any key to exit...
    pause >nul
)

deactivate
