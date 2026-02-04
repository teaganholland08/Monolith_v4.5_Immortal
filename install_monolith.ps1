# --- PROJECT MONOLITH: OMEGA INSTALLER (POWERSHELL EDITION) ---
Write-Host " [1] BUILDING FORTRESS ARCHITECTURE..." -ForegroundColor Green

# 1. CREATE DIRECTORIES
$dirs = @(
    "C:\Monolith",
    "C:\Monolith\System\Agents",
    "C:\Monolith\System\Blueprint",
    "C:\Monolith\System\Scripts",
    "C:\Monolith\System\UI",
    "C:\Monolith\System\Personal",
    "C:\Monolith\Data\Logs",
    "C:\Monolith\Data\Offline_Ark",
    "C:\Monolith\Data\Treasury"
)

foreach ($d in $dirs) {
    if (-not (Test-Path $d)) { New-Item -ItemType Directory -Force -Path $d | Out-Null }
}

# 2. WRITE DASHBOARD CODE (monolith_ui.py)
Write-Host " [2] WRITING AI AGENT CODE..." -ForegroundColor Green
$ui_code = @'
import streamlit as st
import random

st.set_page_config(page_title='MONOLITH COMMAND', layout='wide', page_icon='🏴')
st.title('🏴 PROJECT MONOLITH: OMEGA')
st.markdown('*Total Sovereignty System // Status: ACTIVE*')
st.divider()

col1, col2, col3 = st.columns(3)
col1.metric('HYDRA REVENUE', '$0.00', 'Hunting...')
col2.metric('BODY BATTERY', '92%', 'Peak')
col3.metric('DEFCON LEVEL', '5', 'Safe')

st.subheader('⚡ COMMAND DECK')
c1, c2, c3 = st.columns(3)

if c1.button('LAUNCH HYDRA (Find Money)'):
    st.toast('Deployed Scout Agent...')
    st.write('>> Scanning Arbitrage Vectors...')

if c2.button('LAUNCH SENTINEL (Scan Threats)'):
    st.toast('Deployed Sentinel...')
    st.write('>> Scanning Geopolitics...')

if c3.button('PROTOCOL: FREEDOM'):
    st.success('NOTIFICATIONS SILENCED. ENJOY YOUR DAY.')
'@
Set-Content -Path "C:\Monolith\System\UI\monolith_ui.py" -Value $ui_code -Encoding UTF8

# 3. WRITE HYDRA ENGINE CODE (hydra_main.py)
$hydra_code = @'
import os
from crewai import Agent, Task, Crew, Process
from langchain_community.tools import DuckDuckGoSearchRun

print('## 🏴 PROJECT MONOLITH: HYDRA ENGINE ACTIVE ##')
print('## SCANNING GLOBAL MARKETS FOR ARBITRAGE... ##')
'@
Set-Content -Path "C:\Monolith\System\Scripts\hydra_main.py" -Value $hydra_code -Encoding UTF8

# 4. WRITE REQUIREMENTS
$reqs = "crewai`nlangchain`nstreamlit`npandas`nrequests`nduckduckgo-search`npython-dotenv"
Set-Content -Path "C:\Monolith\requirements.txt" -Value $reqs -Encoding UTF8

# 5. SET ENVIRONMENT VARIABLES
Write-Host " [3] SETTING UP ENVIRONMENT..." -ForegroundColor Green
[System.Environment]::SetEnvironmentVariable("MONOLITH_HOME", "C:\Monolith", "User")
[System.Environment]::SetEnvironmentVariable("MONOLITH_STATUS", "ACTIVE", "User")

# 6. CHECK PYTHON & INSTALL
Write-Host " [4] CHECKING PYTHON..." -ForegroundColor Green
try {
    $pyVersion = python --version 2>&1
    if ($pyVersion) {
        Write-Host "     > Python found: $pyVersion" -ForegroundColor Gray
        Write-Host " [5] INSTALLING DEPENDENCIES..." -ForegroundColor Green
        pip install -r C:\Monolith\requirements.txt
    } else {
        Write-Warning "PYTHON NOT FOUND. Please install Python from python.org and run 'pip install -r C:\Monolith\requirements.txt'"
    }
} catch {
    Write-Warning "Error checking Python. Ensure it is installed and added to PATH."
}

# 7. LAUNCH
Write-Host " [SUCCESS] SYSTEM DEPLOYED." -ForegroundColor Yellow
Write-Host " [ACTION] LAUNCHING DASHBOARD..." -ForegroundColor Yellow
Start-Sleep -Seconds 2
Set-Location "C:\Monolith"
# Using Start-Process to keep it separate or just running it? The user's script just runs it.
# I will leave it as is to be faithful to the request, but be aware it blocks.
streamlit run System\UI\monolith_ui.py
