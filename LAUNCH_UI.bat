@echo off
title MONOLITH: DASHBOARD LAUNCHER
color 0A

echo.
echo [SYSTEM] INITIALIZING INTERFACE...
echo [SYSTEM] CONNECTING TO LOCAL HOST...
echo.

cd /d C:\Monolith
streamlit run System\UI\monolith_ui.py
