@echo off
REM Parking Space Detection Web App Launcher
REM Windows batch script to easily run the Streamlit app

echo.
echo ========================================
echo   Parking Space Detection Web App
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if Streamlit is installed
python -m pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo Installing Streamlit...
    python -m pip install streamlit
    if errorlevel 1 (
        echo Error: Failed to install Streamlit
        pause
        exit /b 1
    )
)

REM Check if model exists
if not exist "module4_deep_learning\resnet18_parking.pth" (
    echo.
    echo Error: Trained model not found at:
    echo   module4_deep_learning\resnet18_parking.pth
    echo.
    echo Please ensure the model file exists and try again.
    pause
    exit /b 1
)

echo.
echo Starting Parking Space Detection Web App...
echo.
echo ✓ Opening browser at: http://localhost:8501
echo ✓ Press Ctrl+C to stop the server
echo.
echo ========================================
echo.

REM Run Streamlit app
python -m streamlit run app.py --logger.level=warning

pause
