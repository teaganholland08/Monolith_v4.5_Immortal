@echo off
REM Windows 11 2026 Privacy Hardening Script
REM Disables telemetry, AI Recall, Cortana, and tracking at kernel level
REM Run as Administrator

title MONOLITH - Windows Privacy Hardening
color 0E

echo ============================================================
echo MONOLITH WINDOWS 11 PRIVACY HARDENING (2026 Edition)
echo ============================================================
echo.
echo This script will:
echo  - Disable Windows Telemetry (DiagTrack, Connected Experiences)
echo  - Remove AI Recall snapshots and disable future captures
echo  - Disable Cortana and copilot
echo  - Stop Windows Update tracking
echo  - Disable location tracking
echo  - Harden privacy settings
echo.
echo WARNING: Run as Administrator
echo.
pause

REM Check for admin
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This script must be run as Administrator
    pause
    exit /b 1
)

echo.
echo [1/10] Disabling Telemetry Services...
sc stop DiagTrack
sc config DiagTrack start= disabled
sc stop dmwappushservice
sc config dmwappushservice start= disabled
sc stop RetailDemo
sc config RetailDemo start= disabled

echo [2/10] Disabling AI Recall...
REM Windows 11 24H2+ AI Recall
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsAI" /v DisableAIDataAnalysis /t REG_DWORD /d 1 /f
reg add "HKCU\Software\Policies\Microsoft\Windows\WindowsAI" /v DisableAIDataAnalysis /t REG_DWORD /d 1 /f
REM Delete existing snapshots
del /f /s /q "%LocalAppData%\CoreAIPlatform.00\UKP\*.*" 2>nul

echo [3/10] Disabling Connected User Experiences...
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\System" /v EnableActivityFeed /t REG_DWORD /d 0 /f
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\System" /v PublishUserActivities /t REG_DWORD /d 0 /f
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\System" /v UploadUserActivities /t REG_DWORD /d 0 /f

echo [4/10] Disabling Cortana...
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\Windows Search" /v AllowCortana /t REG_DWORD /d 0 /f
reg add "HKLM\SOFTWARE\Microsoft\PolicyManager\default\Experience\AllowCortana" /v value /t REG_DWORD /d 0 /f

echo [5/10] Disabling Windows Copilot...
reg add "HKCU\Software\Policies\Microsoft\Windows\WindowsCopilot" /v TurnOffWindowsCopilot /t REG_DWORD /d 1 /f
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsCopilot" /v TurnOffWindowsCopilot /t REG_DWORD /d 1 /f

echo [6/10] Disabling Location Tracking...
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\location" /v Value /t REG_SZ /d Deny /f
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\LocationAndSensors" /v DisableLocation /t REG_DWORD /d 1 /f

echo [7/10] Disabling Advertising ID...
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\AdvertisingInfo" /v Enabled /t REG_DWORD /d 0 /f
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\AdvertisingInfo" /v DisabledByGroupPolicy /t REG_DWORD /d 1 /f

echo [8/10] Disabling Windows Update telemetry...
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection" /v AllowTelemetry /t REG_DWORD /d 0 /f
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection" /v DoNotShowFeedbackNotifications /t REG_DWORD /d 1 /f

echo [9/10] Disabling Windows Error Reporting...
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\Windows Error Reporting" /v Disabled /t REG_DWORD /d 1 /f
reg add "HKLM\SOFTWARE\Microsoft\Windows\Windows Error Reporting" /v Disabled /t REG_DWORD /d 1 /f

echo [10/10] Disabling WiFi Sense (shares WiFi with contacts)...
reg add "HKLM\SOFTWARE\Microsoft\WcmSvc\wifinetworkmanager\config" /v AutoConnectAllowedOEM /t REG_DWORD /d 0 /f

echo.
echo ============================================================
echo PRIVACY HARDENING COMPLETE
echo ============================================================
echo.
echo Changes applied:
echo  [X] Telemetry services disabled
echo  [X] AI Recall disabled and snapshots deleted
echo  [X] Connected User Experiences disabled
echo  [X] Cortana disabled
echo  [X] Windows Copilot disabled
echo  [X] Location tracking disabled
echo  [X] Advertising ID disabled
echo  [X] Update telemetry disabled
echo  [X] Error reporting disabled
echo  [X] WiFi Sense disabled
echo.
echo REBOOT REQUIRED for all changes to take effect.
echo.
pause

echo Rebooting in 30 seconds... (Press Ctrl+C to cancel)
shutdown /r /t 30
