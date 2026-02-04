@echo off
REM MONOLITH WINDOWS DEBLOAT SCRIPT
REM Removes telemetry, bloatware, and hardens Windows for stealth operation
REM Run as Administrator

title MONOLITH: Windows Hardening Protocol
color 0A

echo ========================================
echo   MONOLITH WINDOWS DEBLOAT v1.0
echo   LEVEL 2 (GHOST) HARDENING
echo ========================================
echo.
echo This will:
echo   - Remove Windows bloatware
echo   - Disable telemetry/tracking
echo   - Harden privacy settings
echo   - Optimize performance
echo.
echo Press any key to continue...
pause >nul

echo.
echo [1/5] Removing Bloatware Apps...
echo ----------------------------------------

REM Remove pre-installed Microsoft bloat
PowerShell -Command "Get-AppxPackage *3dbuilder* | Remove-AppxPackage"
PowerShell -Command "Get-AppxPackage *windowsmaps* | Remove-AppxPackage"
PowerShell -Command "Get-AppxPackage *bingweather* | Remove-AppxPackage"
PowerShell -Command "Get-AppxPackage *bingfinance* | Remove-AppxPackage"
PowerShell -Command "Get-AppxPackage *bingnews* | Remove-AppxPackage"
PowerShell -Command "Get-AppxPackage *bingsports* | Remove-AppxPackage"
PowerShell -Command "Get-AppxPackage *zunemusic* | Remove-AppxPackage"
PowerShell -Command "Get-AppxPackage *zunevideo* | Remove-AppxPackage"
PowerShell -Command "Get-AppxPackage *windowsphone* | Remove-AppxPackage"
PowerShell -Command "Get-AppxPackage *solitairecollection* | Remove-AppxPackage"
PowerShell -Command "Get-AppxPackage *officehub* | Remove-AppxPackage"
PowerShell -Command "Get-AppxPackage *skypeapp* | Remove-AppxPackage"
PowerShell -Command "Get-AppxPackage *getstarted* | Remove-AppxPackage"
PowerShell -Command "Get-AppxPackage *windowsfeedbackhub* | Remove-AppxPackage"
PowerShell -Command "Get-AppxPackage *people* | Remove-AppxPackage"
PowerShell -Command "Get-AppxPackage *soundrecorder* | Remove-AppxPackage"
PowerShell -Command "Get-AppxPackage *xboxapp* | Remove-AppxPackage"

echo Done.

echo.
echo [2/5] Disabling Telemetry Services...
echo ----------------------------------------

REM Disable telemetry/diagnostics
sc config "DiagTrack" start= disabled
sc stop "DiagTrack"
sc config "dmwappushservice" start= disabled
sc stop "dmwappushservice"
sc config "WerSvc" start= disabled
sc stop "WerSvc"

echo Done.

echo.
echo [3/5] Hardening Privacy Settings...
echo ----------------------------------------

REM Disable data collection
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\DataCollection" /v AllowTelemetry /t REG_DWORD /d 0 /f
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection" /v AllowTelemetry /t REG_DWORD /d 0 /f

REM Disable Cortana
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\Windows Search" /v AllowCortana /t REG_DWORD /d 0 /f

REM Disable location tracking
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\location" /v Value /t REG_SZ /d Deny /f

REM Disable advertising ID
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\AdvertisingInfo" /v Enabled /t REG_DWORD /d 0 /f

REM Disable activity history
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\System" /v PublishUserActivities /t REG_DWORD /d 0 /f

REM Disable timeline
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\System" /v EnableActivityFeed /t REG_DWORD /d 0 /f

echo Done.

echo.
echo [4/5] Disabling Unnecessary Services...
echo ----------------------------------------

REM Windows Update (re-enable manually when needed)
sc config "wuauserv" start= disabled
sc stop "wuauserv"

REM Windows Search (use Everything instead)
sc config "WSearch" start= disabled
sc stop "WSearch"

REM Remote Registry (security risk)
sc config "RemoteRegistry" start= disabled
sc stop "RemoteRegistry"

echo Done.

echo.
echo [5/5] Cleaning Temp Files...
echo ----------------------------------------

del /f /s /q %temp%\*.* 2>nul
del /f /s /q C:\Windows\Temp\*.* 2>nul
del /f /s /q %userprofile%\AppData\Local\Temp\*.* 2>nul

echo Done.

echo.
echo ========================================
echo   DEBLOAT COMPLETE
echo ========================================
echo.
echo NEXT STEPS:
echo   1. Restart your computer
echo   2. Install Surfshark VPN (or similar)
echo   3. Set GUMROAD_ACCESS_TOKEN env variable
echo   4. Launch Monolith
echo.
echo PRIVACY RECOMMENDATIONS:
echo   - Use Firefox with uBlock Origin
echo   - Use Privacy.com for payments
echo   - Use ProtonMail for email
echo   - Consider Tails OS for max anonymity
echo.
pause
