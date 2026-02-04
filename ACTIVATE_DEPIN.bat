@echo off
title PROJECT MONOLITH: DePIN Activation (ZERO CAPITAL)
color 0A

echo ==============================
echo   DEPIN MONETIZATION SETUP
echo   Starting from $0
echo ==============================
echo.

echo [1/3] Checking GPU...
nvidia-smi --query-gpu=name --format=csv,noheader
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: NVIDIA GPU not detected. io.net requires NVIDIA.
    pause
    exit /b 1
)
echo GPU: CONFIRMED

echo.
echo [2/3] Opening io.net signup...
start https://cloud.io.net/worker
echo.
echo MANUAL STEP REQUIRED:
echo 1. Create account (no payment needed)
echo 2. Copy your Worker ID
echo 3. Download io-worker for Windows
echo.
pause

echo.
echo [3/3] Opening Grass extension...
start https://chromewebstore.google.com/detail/grass/ilehaonighjijnmpnagapkhpcdbhclfg
echo.
echo MANUAL STEP REQUIRED:
echo 1. Click "Add to Chrome"
echo 2. Create account (email only)
echo 3. Click "Start" to begin earning
echo.
pause

echo.
echo ==============================================================
echo   SETUP COMPLETE
echo   Check System\Logs\Treasury\execution_log.jsonl for earnings
echo ==============================================================
pause
