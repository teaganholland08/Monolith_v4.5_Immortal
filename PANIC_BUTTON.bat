@echo off
REM MONOLITH PANIC BUTTON - EMERGENCY DATA WIPE
REM WARNING: THIS WILL PERMANENTLY DELETE SENSITIVE DATA
REM Use only in genuine emergency situations

title MONOLITH: PANIC PROTOCOL ACTIVATED
color 0C

echo.
echo ========================================
echo   ⚠️  PANIC BUTTON ACTIVATED  ⚠️
echo ========================================
echo.
echo This will PERMANENTLY DELETE:
echo   - Brain/Vault folder (encrypted assets)
echo   - System/Logs folder (all activity logs)
echo   - Temp files and browser cache
echo   - Recent files history
echo.
echo Press CTRL+C to CANCEL within 10 seconds...
echo.

timeout /t 10 /nobreak

echo.
echo [PHASE 1] STOPPING ALL MONOLITH PROCESSES
echo ========================================
taskkill /F /IM python.exe 2>nul
taskkill /F /IM chrome.exe 2>nul
taskkill /F /IM firefox.exe 2>nul
taskkill /F /IM msedge.exe 2>nul
echo ✓ Processes terminated

echo.
echo [PHASE 2] SECURE DELETION (NIST 800-88 Method)
echo ========================================

REM Use cipher /w for secure deletion (3-pass DoD standard)
REM This overwrites free space making recovery impossible

cd "%USERPROFILE%\Desktop\Monolith_v4.5_Immortal"

REM Delete vault
if exist "Brain\Vault" (
    echo Wiping Brain/Vault...
    del /F /S /Q "Brain\Vault\*.*" 2>nul
    cipher /w:Brain\Vault
    rd /S /Q "Brain\Vault" 2>nul
    echo ✓ Vault wiped
)

REM Delete logs
if exist "System\Logs" (
    echo Wiping System/Logs...
    del /F /S /Q "System\Logs\*.*" 2>nul
    cipher /w:System\Logs
    rd /S /Q "System\Logs" 2>nul
    echo ✓ Logs wiped
)

REM Delete revenue tracking
if exist "System\Logs\ledger.db" (
    del /F "System\Logs\ledger.db" 2>nul
    echo ✓ Ledger deleted
)

REM Delete generated assets
if exist "Assets" (
    echo Wiping Assets...
    del /F /S /Q "Assets\*.*" 2>nul
    cipher /w:Assets
    echo ✓ Assets wiped
)

echo.
echo [PHASE 3] SYSTEM FORENSIC CLEANUP
echo ========================================

REM Clear temp files
del /F /S /Q %temp%\*.* 2>nul
del /F /S /Q C:\Windows\Temp\*.* 2>nul

REM Clear recent files
del /F /S /Q "%APPDATA%\Microsoft\Windows\Recent\*.*" 2>nul

REM Clear browser cache (Chrome)
if exist "%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache" (
    del /F /S /Q "%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache\*.*" 2>nul
)

REM Clear clipboard
echo off | clip

REM Clear PowerShell history
if exist "%APPDATA%\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt" (
    del /F "%APPDATA%\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt" 2>nul
)

echo ✓ Forensic cleanup complete

echo.
echo [PHASE 4] NETWORK DISCONNECT
echo ========================================
netsh interface set interface "Wi-Fi" admin=disable 2>nul
netsh interface set interface "Ethernet" admin=disable 2>nul
echo ✓ All network adapters disabled

echo.
echo ========================================
echo   PANIC PROTOCOL COMPLETE
echo ========================================
echo.
echo DATA STATUS:
echo   Vault:    WIPED
echo   Logs:     WIPED
echo   Assets:   WIPED
echo   Network:  DISCONNECTED
echo.
echo NEXT STEPS:
echo   1. Remove USB backup drive (if present)
echo   2. Place phone in Faraday bag
echo   3. Execute physical relocation
echo   4. Use Go-Bag for off-grid operation
echo.
echo Press any key to lock workstation...
pause >nul

rundll32.exe user32.dll,LockWorkStation
