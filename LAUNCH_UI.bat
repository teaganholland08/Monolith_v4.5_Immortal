@echo off
title MONOLITH COMMAND CENTER
color 0B
echo ==================================================
echo   LAUNCHING MONOLITH SOVEREIGN INTERFACE
echo ==================================================
echo.
echo [1/2] Starting TUI (Terminal Interface)...
start "MONOLITH TUI" python monolith_dashboard_tui.py
echo.
echo [2/2] Starting Web Dashboard (Streamlit)...
streamlit run monolith_dashboard.py
pause
