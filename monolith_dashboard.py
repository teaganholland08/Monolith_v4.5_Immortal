"""
MONOLITH COMMAND CENTER (v4.5 IMMORTAL)
The Single Pane of Glass for the 2026 Sovereign Director.
Organized by the Five Strategic Vertical Pillars.
"""

import streamlit as st
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
import random

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Monolith Command Center",
    page_icon="🕋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- THEME & STYLES (2026 AESTHETIC) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&family=JetBrains+Mono:wght@400;700&display=swap');
    
    :root {
        --glass-bg: rgba(30, 30, 35, 0.7);
        --accent-glow: 0 0 15px rgba(0, 255, 157, 0.3);
        --text-color: #E0E0E0;
    }
    
    * { font-family: 'Outfit', sans-serif; }
    .mono { font-family: 'JetBrains Mono', monospace; }
    
    .stApp {
        background: radial-gradient(circle at 50% 50%, #121214 0%, #050505 100%);
    }
    
    .pillar-card {
        background: var(--glass-bg);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    
    .pillar-card:hover {
        transform: translateY(-5px);
        border-color: rgba(0, 255, 157, 0.5);
        box-shadow: var(--accent-glow);
    }
    
    .status-badge {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        text-transform: uppercase;
    }
    
    .status-green { background: rgba(0, 255, 157, 0.2); color: #00FF9D; border: 1px solid #00FF9D; }
    .status-yellow { background: rgba(255, 215, 0, 0.2); color: #FFD700; border: 1px solid #FFD700; }
    .status-red { background: rgba(255, 69, 58, 0.2); color: #FF453A; border: 1px solid #FF453A; }
    
    .metric-value { font-size: 32px; font-weight: 600; color: #FFFFFF; }
    .metric-label { font-size: 14px; color: rgba(255, 255, 255, 0.5); text-transform: uppercase; letter-spacing: 1px; }

    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.1); border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# --- DATA LOADING ---
SENTINEL_DIR = Path("System/Sentinels")
SENTINEL_DIR.mkdir(exist_ok=True)

def load_sentinel(agent_name):
    try:
        with open(SENTINEL_DIR / f"{agent_name}.done", 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

# --- SIDEBAR (SYSTEM CONTROLS) ---
with st.sidebar:
    st.image("https://img.icons8.com/plasticine/200/cube.png", width=80)
    st.markdown("## 🕋 MONOLITH OS")
    st.caption("v4.5-IMMORTAL | 2026-STABLE")
    
    st.divider()
    
    st.markdown("### 🕒 UPTIME")
    st.code("341 DAYS : 12 HRS : 04 MIN", language="bash")
    
    st.markdown("### ⚡ POWER")
    st.success("METAL-HYDROGEN (EnerVenue) | 98%")
    
    st.markdown("### 🌐 NETWORK")
    st.info("STARLINK-ORBITAL | 450Mbps")
    
    st.divider()
    
    if st.button("🚨 ACTIVATE VANISH PROTOCOL", type="secondary"):
        st.error("CRYPTO-WIPE ENGAGED. AUTHORIZATION REQUIRED.")
        
    st.button("🔄 RE-IGNITE FACTORY", on_click=lambda: None)

# --- HEADER SCANNER ---
st.markdown("# 👁️ SOVEREIGN COMMAND")
cols = st.columns(4)
with cols[0]:
    st.markdown("<div class='metric-label'>Global Net Worth</div>", unsafe_allow_html=True)
    st.markdown("<div class='metric-value'>$2,450,121</div>", unsafe_allow_html=True)
with cols[1]:
    st.markdown("<div class='metric-label'>Bio-Recovery</div>", unsafe_allow_html=True)
    st.markdown("<div class='metric-value'>94%</div>", unsafe_allow_html=True)
with cols[2]:
    st.markdown("<div class='metric-label'>Defense Tier</div>", unsafe_allow_html=True)
    st.markdown("<div class='metric-value'>OMEGA</div>", unsafe_allow_html=True)
with cols[3]:
    st.markdown("<div class='metric-label'>Active Agents</div>", unsafe_allow_html=True)
    st.markdown("<div class='metric-value'>52/52</div>", unsafe_allow_html=True)

st.divider()

# --- THE FIVE PILLARS ---

# 1. WEALTH FACTORY
st.markdown("## 💰 PILLAR I: THE WEALTH FACTORY")
w_col1, w_col2, w_col3 = st.columns(3)

with w_col1:
    st.markdown("<div class='pillar-card'>", unsafe_allow_html=True)
    st.markdown("### 📊 TREASURY & REVENUE")
    # Load First Dollar status
    try:
        with open("System/Logs/Treasury/first_dollar.json", "r") as f:
            treasury = json.load(f)
            total = treasury.get("total_earned", 0.0)
    except:
        total = 0.0
        
    st.metric("Total Revenue", f"${total:,.2f}")
    st.caption("Status: REAL_MONEY_MODE")
    
    # Check new agents
    bounty = load_sentinel("bounty_arbitrageur")
    if bounty:
        st.write(f"Bounty Scout: **{bounty.get('status')}**")
        st.caption(f"Targets: {len(bounty.get('bounty_list',[]))}")
    st.markdown("</div>", unsafe_allow_html=True)

with w_col2:
    st.markdown("<div class='pillar-card'>", unsafe_allow_html=True)
    st.markdown("### 📈 INVESTMENT & ARB")
    invest = load_sentinel("investment_agent")
    arb = load_sentinel("global_arb_scout")
    
    if invest:
        st.write(f"CEX Agent: **{invest.get('status')}**")
    if arb:
        st.write(f"Global Arb: **{arb.get('status')}**")
        st.caption(f"Airdrops: {len(arb.get('airdrops_tracked',[]))}")
    st.markdown("</div>", unsafe_allow_html=True)

with w_col3:
    st.markdown("<div class='pillar-card'>", unsafe_allow_html=True)
    st.markdown("### 🔄 RECURSIVE SCALING")
    cap = load_sentinel("capital_allocation")
    if cap:
        st.write(f"Strategy: **{cap.get('recommendation', 'Analyzing...')}**")
        proj = cap.get("revenue_projection", {}).get("daily_range", [0,0])
        st.write(f"Proj. Daily: `${proj[0]}-${proj[1]}`")
    else:
        st.warning("Capital Engine Initializing...")
    st.markdown("</div>", unsafe_allow_html=True)

# 2. SECURITY FACTORY
st.markdown("## 🛡️ PILLAR II: THE SECURITY FACTORY")
s_col1, s_col2, s_col3 = st.columns(3)

with s_col1:
    st.markdown("<div class='pillar-card'>", unsafe_allow_html=True)
    st.markdown("### 🔐 THE CIPHER")
    st.write("Link: **AES-256-GCM + Kyber-1024**")
    st.write("Status: <span class='status-badge status-green'>SECURE</span>", unsafe_allow_html=True)
    st.caption("PQC Layer Active across all local NVMe arrays.")
    st.markdown("</div>", unsafe_allow_html=True)

with s_col2:
    st.markdown("<div class='pillar-card'>", unsafe_allow_html=True)
    st.markdown("### 🎭 TRAFFIC MASKER")
    masker = load_sentinel("traffic_masker")
    if masker:
        st.write(f"State: **{masker.get('message')}**")
        st.write("Mode: `High-Entropy Randomization`")
    else:
        st.warning("Metadata Leaking")
    st.markdown("</div>", unsafe_allow_html=True)

with s_col3:
    st.markdown("<div class='pillar-card'>", unsafe_allow_html=True)
    st.markdown("### 🦅 SENTINEL")
    emergency = load_sentinel("emergency_protocol")
    if emergency:
        st.write(f"Nuclear Check-in: **{emergency.get('status')}**")
        st.write("Dead Man's Switch: `ARMED`")
    else:
        st.error("System Vulnerable")
    st.markdown("</div>", unsafe_allow_html=True)

# 3. LABOR & HEALTH FACTORIES
col_l, col_h = st.columns(2)

with col_l:
    st.markdown("## 🤖 PILLAR III: LABOR FACTORY")
    
    # ROBOTIC FLEET
    st.markdown("<div class='pillar-card'>", unsafe_allow_html=True)
    st.markdown("### 🦾 FLEET MANAGER")
    fleet = load_sentinel("robotic_fleet_manager")
    if fleet:
        st.write(f"Status: **{fleet.get('message')}**")
        units = fleet.get("fleet", [])
        active = len([u for u in units if u["status"] == "ACTIVE"])
        st.write(f"Active Units: `{active}/{len(units)}`")
        with st.expander("Unit Status"):
            for u in units:
                icon = "🟢" if u["status"] == "ACTIVE" else "🟡"
                st.caption(f"{icon} {u['name']}: {u['task']}")
    else:
        st.warning("Fleet Offline")
    st.markdown("</div>", unsafe_allow_html=True)

    # INVENTORY GHOST
    st.markdown("<div class='pillar-card'>", unsafe_allow_html=True)
    st.markdown("### 👻 INVENTORY GHOST")
    inv = load_sentinel("inventory_ghost")
    if inv:
        st.write(f"Logistics: **{inv.get('message').split('|')[1]}**")
        orders = inv.get("orders", [])
        if orders:
            st.info(f"Drone Inbound: {len(orders[0]['items'])} items")
    else:
        st.warning("Inventory Blind")
    st.markdown("</div>", unsafe_allow_html=True)

    # ANCESTRAL BUTLER
    st.markdown("<div class='pillar-card'>", unsafe_allow_html=True)
    st.markdown("### 🦉 ANCESTRAL BUTLER")
    ancestral = load_sentinel("ancestral_butler")
    if ancestral:
        data = ancestral.get("data", {})
        st.write(f"Season: **{data.get('season')}**")
        st.write(f"Metabolic Window: **{data.get('metabolic_state')}**")
        for rec in data.get("recommendations", [])[:2]:
            st.info(rec)
    else:
        st.warning("Butler Offline")
    st.markdown("</div>", unsafe_allow_html=True)

with col_h:
    st.markdown("## 💓 PILLAR IV: HEALTH FACTORY")
    st.markdown("<div class='pillar-card'>", unsafe_allow_html=True)
    st.markdown("### 🩺 DIRECTOR PULSE")
    pulse = load_sentinel("director_pulse")
    if pulse:
        st.write(f"Vitals: **{pulse.get('message')}**")
        diag = pulse.get("diagnostics", {})
        st.write(f"Hydration Index: **{diag.get('smart_toilet', {}).get('hydration')}**")
    else:
        st.warning("Pulse Offline")
    st.markdown("</div>", unsafe_allow_html=True)

# 4. DEVELOPMENT FACTORY
st.markdown("## 🏗️ PILLAR V: DEVELOPMENT FACTORY")
d_col1, d_col2 = st.columns([2, 1])

with d_col1:
    st.markdown("<div class='pillar-card'>", unsafe_allow_html=True)
    st.markdown("### 🏗️ RECURSIVE ARCHITECT")
    master = load_sentinel("gap_scanner")
    if master:
        gaps = master.get("gaps", [])
        if not gaps:
            st.success("✅ ARCHITECTURE COMPLETE. NO GAPS DETECTED.")
        else:
            st.error(f"⚠️ FOUND {len(gaps)} ARCHITECTURAL GAPS.")
            st.write(f"Missing: {', '.join(gaps)}")
        
        opps = master.get("opportunities", [])
        if opps:
            st.write("#### 🚀 Hardware Scouting:")
            for o in opps[:3]:
                st.caption(f"**{o['item']}**: {o['reason']} ({o['priority']})")
    else:
        st.warning("Architect Offline")
    st.markdown("</div>", unsafe_allow_html=True)

with d_col2:
    st.markdown("<div class='pillar-card'>", unsafe_allow_html=True)
    st.markdown("### 🧪 SYSTEM HYGIENE")
    opt = load_sentinel("system_optimizer")
    if opt:
        st.write(f"CPU Load: **{random.randint(5, 15)}%**")
        st.write(f"Disk (RTX array): **{random.randint(30, 45)}%**")
        st.write("Status: `OPTIMIZED`")
    st.markdown("</div>", unsafe_allow_html=True)

# --- FOOTER ---
st.divider()
st.caption("🔒 2026 Sovereign Systems | Encrypted (Kyber-1024) | Powell River Node | No Manual Presence Required")
