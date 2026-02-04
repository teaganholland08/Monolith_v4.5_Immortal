@echo off
title PROJECT MONOLITH: OMEGA DEPLOYMENT
color 0A

echo ========================================================
echo   PROJECT MONOLITH: OMEGA EDITION (v4.5 IMMORTAL)
echo ========================================================
echo.
echo   [1] VERIFYING FORTRESS ARCHITECTURE...
echo   [2] ACTIVATING AGENCY PROTOCOLS (Hydra, Moltbot)...
echo   [3] SYNCING NEURAL PATHWAYS...
echo.

:: --- 1. SET ENVIRONMENT ---
set BASE_DIR=%~dp0
cd /d "%BASE_DIR%"

:: --- 2. INSTALL DEPENDENCIES ---
echo [SYSTEM] INSTALLING NEURAL PATHWAYS...
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [WARNING] PIP INSTALL FAILED. CHECK PYTHON INSTALLATION.
    pause
    exit
)

:: --- 3. LAUNCH SEQUENCE ---
echo.
echo [SUCCESS] AGENCY READY.
echo [ACTION] LAUNCHING COMMAND DASHBOARD & OMEGA KERNEL...

:: Launch Dashboard in background
start /B streamlit run System/UI/monolith_ui.py

:: Launch Kernel in this window
echo.
echo [KERNEL] IGNITING MONOLITH OMEGA...
python monolith_omega.py

pause