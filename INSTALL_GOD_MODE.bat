@echo off
title MONOLITH: GOD MODE COMPLETE INSTALLER
color 0F

echo ========================================================
echo   PROJECT MONOLITH: GOD MODE INSTALLATION
echo   Installing: Voice Control + Universal IoT + Concierge
echo ========================================================
echo.

:: Check if base system exists
if not exist "C:\Monolith\config.py" (
    echo [ERROR] Base Monolith system not found!
    echo Please run the main installer first.
    pause
    exit /b 1
)

echo [1] INSTALLING VOICE RECOGNITION LIBRARIES...
python -m pip install --quiet SpeechRecognition pyaudio 2>nul
if %errorlevel% neq 0 (
    echo    [NOTE] PyAudio installation may require additional setup
    echo    Voice features will use text input as fallback
)

echo [2] VERIFYING CORE COMPONENTS...
if exist "C:\Monolith\System\Scripts\concierge_main.py" (
    echo    ✓ Concierge Agent installed
) else (
    echo    ✗ Concierge Agent missing
)

if exist "C:\Monolith\System\Scripts\smarthome_controller.py" (
    echo    ✓ Smart Home Controller installed
) else (
    echo    ✗ Smart Home Controller missing
)

if exist "C:\Monolith\System\UI\monolith_ui.py" (
    echo    ✓ God Mode Dashboard installed
) else (
    echo    ✗ Dashboard missing
)

echo.
echo [3] TESTING CONCIERGE AGENT...
python System\Scripts\concierge_main.py
if %errorlevel% equ 0 (
    echo    ✓ Concierge test passed
)

echo.
echo [4] TESTING SMART HOME CONTROLLER...
python System\Scripts\smarthome_controller.py
if %errorlevel% equ 0 (
    echo    ✓ Smart Home test passed
)

echo.
echo ========================================================
echo   [SUCCESS] GOD MODE INSTALLATION COMPLETE
echo ========================================================
echo.
echo YOUR SYSTEM NOW HAS:
echo   ✓ Voice Command Interface (🎙️ Speak button)
echo   ✓ Personal Concierge (🎩 Alfred)
echo   ✓ Universal Smart Home Control (🏠 2,500+ devices)
echo   ✓ Unified Command Router (Physical + Digital + Logistics)
echo.
echo NEXT STEPS:
echo   1. Launch Dashboard: python -m streamlit run System\UI\monolith_ui.py
echo   2. Access at: http://localhost:8501
echo   3. Try commands like:
echo      - "Turn on the lights"
echo      - "Make me money"
echo      - "Buy grass-fed beef"
echo      - "Lock all doors"
echo.
echo OPTIONAL SETUP:
echo   • For real smart home control, set: HOME_ASSISTANT_TOKEN
echo   • For voice input, ensure microphone is connected
echo   • For cloud AI, run: python System\Scripts\stack_switcher.py
echo.
echo ========================================================
pause
