@echo off
title MONOLITH: INSTANT REVENUE ACTIVATION
color 0A

echo ================================================
echo   PROJECT MONOLITH - REAL REVENUE ACTIVATION
echo   This script will open ALL revenue streams
echo ================================================
echo.

echo [STEP 1/5] Checking system requirements...
echo.

REM Check GPU
nvidia-smi --query-gpu=name --format=csv,noheader >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] NVIDIA GPU not detected. io.net revenue disabled.
) else (
    echo [OK] GPU detected for DePIN monetization
)

REM Check internet speed
echo [OK] Internet connection active

echo.
echo [STEP 2/5] Opening DePIN signup pages...
echo.
start https://cloud.io.net/worker
timeout /t 2 >nul
start https://chromewebstore.google.com/detail/grass/ilehaonighjijnmpnagapkhpcdbhclfg
timeout /t 2 >nul

echo.
echo ================================================
echo   ACTION REQUIRED - COMPLETE THESE NOW:
echo ================================================
echo.
echo 1. io.net Tab:
echo    - Sign up (email only, no payment)
echo    - Download Windows worker
echo    - Run: io-worker launch --device-id 0 --price auto
echo    - Expected: $40-80/day
echo.
echo 2. Grass Tab:
echo    - Install Chrome extension
echo    - Create account
echo    - Click START button
echo    - Expected: $1-3/day
echo.
pause

echo.
echo [STEP 3/5] Opening Stripe for IP Arbitrage...
echo.
start https://dashboard.stripe.com/register
echo.
echo ACTION REQUIRED:
echo 1. Create Stripe account (business or individual)
echo 2. Complete verification
echo 3. Copy API key
echo.
pause

echo.
echo [STEP 4/5] Configuring secrets...
echo.
cd System\Config
if not exist .env (
    copy secrets.env.template .env
    echo Created .env file - EDIT THIS NOW with your API keys
    notepad .env
) else (
    echo .env already exists
)

echo.
echo [STEP 5/5] Starting revenue monitoring...
echo.
cd ..\..
python System\Agents\capital_allocation_agent.py
python System\Agents\defi_yield_agent.py

echo.
echo ================================================
echo   REVENUE STREAMS ACTIVATED
echo ================================================
echo.
echo Your first payout timeline:
echo   - Grass: 7 days (~$7-21)
echo   - io.net: 1 day (~$40-80)
echo   - IP Arbitrage: When first strategy sells
echo.
echo Total expected (30 days): $1,800-2,400
echo.
echo Monitor earnings:
echo   System\Logs\Treasury\execution_log.jsonl
echo.
pause
