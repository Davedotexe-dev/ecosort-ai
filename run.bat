@echo off
title EcoSort AI - 1-Click Launcher
echo ===================================================
echo             Launching EcoSort AI
echo ===================================================
echo.

if exist "venv\Scripts\streamlit.exe" (
    echo Using virtual environment...
    venv\Scripts\streamlit.exe run app.py
) else (
    echo Using system Python / Streamlit...
    streamlit run app.py
)

pause