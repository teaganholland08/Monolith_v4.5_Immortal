@echo off
title PROJECT MONOLITH: DUAL-STACK INSTALLER
color 0A

echo ========================================================
echo   PROJECT MONOLITH: DUAL-STACK ARCHITECTURE
echo ========================================================
echo.
echo   DETECTED STACKS:
echo   [A] LOCAL FORTRESS STACK (Privacy/Offline/Llama-3)
echo   [B] CLOUD GOD MODE STACK (Profit/Online/GPT-5)
echo.
set /p stack=">> CHOOSE STACK TO CONFIGURE (A/B): "

echo.
echo   [1] BUILDING ARCHITECTURE FOLDERS...
if not exist "C:\Monolith" mkdir "C:\Monolith"
if not exist "C:\Monolith\System" mkdir "C:\Monolith\System"
if not exist "C:\Monolith\System\Agents" mkdir "C:\Monolith\System\Agents"
if not exist "C:\Monolith\System\Blueprint" mkdir "C:\Monolith\System\Blueprint"
if not exist "C:\Monolith\System\Scripts" mkdir "C:\Monolith\System\Scripts"
if not exist "C:\Monolith\System\UI" mkdir "C:\Monolith\System\UI"
if not exist "C:\Monolith\Data\Logs" mkdir "C:\Monolith\Data\Logs"
if not exist "C:\Monolith\Data\Offline_Ark" mkdir "C:\Monolith\Data\Offline_Ark"
if not exist "C:\Monolith\Data\Treasury" mkdir "C:\Monolith\Data\Treasury"

echo   [2] GENERATING %stack% SPECIFIC CONFIGURATION...

if /i "%stack%"=="A" (
    set STACK_MODE=LOCAL
    set LLM_MODEL=llama3
    set OBSERVABILITY=Loki
    set MODE_NAME=FORTRESS
) else (
    set STACK_MODE=CLOUD
    set LLM_MODEL=gpt-4o
    set OBSERVABILITY=ELK
    set MODE_NAME=GOD_MODE
)

(
echo import os
echo.
echo # STACK CONFIGURATION
echo STACK_MODE = "%STACK_MODE%"
echo LLM_MODEL = "%LLM_MODEL%"
echo OBSERVABILITY = "%OBSERVABILITY%"
echo MODE_NAME = "%MODE_NAME%"
echo.
echo print^(f"## MONOLITH INITIALIZED IN {STACK_MODE} MODE ##"^)
echo print^(f"## AI Model: {LLM_MODEL} ##"^)
echo print^(f"## Observability: {OBSERVABILITY} ##"^)
) > "C:\Monolith\System\config_generated.py"

echo   [3] SETTING ENVIRONMENT VARIABLES...
setx MONOLITH_HOME "C:\Monolith"
setx MONOLITH_STACK "%STACK_MODE%"
setx MONOLITH_MODE "%MODE_NAME%"

echo   [4] CHECKING PYTHON...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   [WARNING] Python not found! Install from python.org
    goto :end
)

echo   [5] INSTALLING CORE DEPENDENCIES...
echo   (Installing minimal dependencies for quick setup)
python -m pip install streamlit pandas requests python-dotenv --quiet

echo.
echo [SUCCESS] %MODE_NAME% STACK CONFIGURATION COMPLETE!
echo.
echo NEXT STEPS:
echo   1. Run: cd C:\Monolith
echo   2. Run: python config.py (to verify configuration)
echo   3. Run: python System\Scripts\stack_switcher.py (to change modes)
echo   4. Run: python -m streamlit run System\UI\monolith_ui.py (to launch dashboard)
echo.

:end
pause
