@echo off
title Address Variation Generator - Midnightvandal
echo.
echo ============================================
echo   Address Variation Generator
echo   Created by Midnightvandal
echo ============================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during install.
    pause
    exit /b 1
)

python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo Installing required package (streamlit)...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Failed to install requirements.
        pause
        exit /b 1
    )
)

echo Starting app...
echo Open the URL that appears below in your browser.
echo.
streamlit run address_variator_app.py

pause
