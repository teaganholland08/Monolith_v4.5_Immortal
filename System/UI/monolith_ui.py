import streamlit as st
import time
import random
import os

# --- 1. PAGE CONFIGURATION (The Hacker Aesthetic) ---
st.set_page_config(
    page_title="MONOLITH /// GOD MODE",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for the "Command Center" look
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #00ff41; font-family: 'Courier New', monospace; }
    .stMetric { background-color: #1a1c24; padding: 10px; border-radius: 5px; border: 1px solid #333; }
    .stButton > button { background-color: #262730; color: white; border: 1px solid #444; width: 100%; }
    .stTextInput > div > div > input { background-color: #111; color: #00ff41; font-size: 20px; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR (System Status) ---
with st.sidebar:
    st.title("🏴 SYSTEM STATUS")
    st.markdown("---")
    st.write("**CORE:** ACTIVE")
    st.write("**CONN:** ENCRYPTED (VPN)")
    st.write("**DISK:** 12TB / 20TB (Offline Ark)")
    st.markdown("---")
    st.write("### ACTIVE AGENTS")
    st.code("• HYDRA: HUNTING\n• SENTINEL: WATCHING\n• ALFRED: STANDBY")

# --- 3. HEADER & METRICS (The Big 3) ---
st.title("👁️ PROJECT MONOLITH")
st.caption("// OMEGA PROTOCOL ACTIVE")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("HYDRA REVENUE", "$4,420.00", "+$350 Today")
with col2:
    st.metric("BODY BATTERY", "94%", "Peak State")
with col3:
    st.metric("DEFCON LEVEL", "5", "Global Stable")
with col4:
    st.metric("GRID POWER", "100%", "Solar + Battery")

st.markdown("---")

# --- 4. THE GOD BAR (Universal Input) ---
# This single box controls the entire system.
cmd_col, btn_col = st.columns([4, 1])

with cmd_col:
    command = st.text_input("COMMAND LINE", placeholder="Say 'Lights on', 'Make money', or 'Check threats'...")

with btn_col:
    st.write("##") # Spacer
    if st.button("🎙️ SPEAK"):
        st.toast("🎤 Listening... (Voice Module Active)")
        # In real deployment, this triggers speech_recognition logic
        time.sleep(1)
        command = "Simulated Voice Command"

# --- 5. THE ROUTING LOGIC (The Brain) ---
if command:
    st.markdown("### ⚡ ACTION LOG")
    with st.status(f"PROCESSING: '{command}'...", expanded=True) as status:
        time.sleep(1)
        cmd_lower = command.lower()

        # ROUTE A: HYDRA (Money)
        if any(x in cmd_lower for x in ['money', 'profit', 'cash', 'income']):
            st.write("🔍 Analyzing Intent: FINANCIAL GROWTH")
            st.write("🐙 Routing to: **HYDRA ENGINE**")
            time.sleep(1)
            st.json({
                "Target": "Arbitrage Scan",
                "Sector": "Crypto/SaaS",
                "Est. Profit": "$50 - $200",
                "Status": "EXECUTING"
            })
            status.update(label="✅ CAMPAIGN LAUNCHED", state="complete")

        # ROUTE B: IOT (Home)
        elif any(x in cmd_lower for x in ['light', 'door', 'lock', 'temp', 'house']):
            st.write("🔍 Analyzing Intent: PHYSICAL CONTROL")
            st.write("🏠 Routing to: **HOME ASSISTANT API**")
            time.sleep(1)
            st.success(f"PHYSICAL ACTION EXECUTED: {command.upper()}")
            status.update(label="✅ HARDWARE UPDATED", state="complete")

        # ROUTE C: SHADOW (Survival)
        elif any(x in cmd_lower for x in ['danger', 'threat', 'war', 'grid']):
            st.write("🔍 Analyzing Intent: SECURITY AUDIT")
            st.write("🌑 Routing to: **THE SHADOW**")
            time.sleep(1)
            st.warning("Scanning Global News Feeds...")
            st.info("RESULT: No Immediate Threats Detected.")
            status.update(label="✅ PERIMETER SECURE", state="complete")

        # ROUTE D: GENERAL (LLM)
        else:
            st.write("🔍 Analyzing Intent: GENERAL QUERY")
            st.write("🧠 Routing to: **LOCAL LLM (Llama-3)**")
            time.sleep(1)
            st.info(f"Thinking about '{command}'...")
            status.update(label="✅ RESPONSE GENERATED", state="complete")

# --- 6. VISUAL DATA DECKS (Tabs) ---
st.markdown("---")
tab1, tab2, tab3 = st.tabs(["🐙 HYDRA DECK", "🏠 SMART HOME", "🌑 SHADOW NET"])

with tab1:
    st.subheader("REVENUE STREAMS")
    st.dataframe({
        "VECTOR": ["Factory (Assets)", "Broadcaster (Media)", "Middleman (Arb)", "Trader (Yield)"],
        "STATUS": ["Active", "Active", "Scanning", "Holding"],
        "DAILY PROFIT": ["$120", "$50", "$0", "$180"]
    }, use_container_width=True)
    if st.button("REBOOT HYDRA"):
        st.toast("Restarting Revenue Swarm...")

with tab2:
    st.subheader("PHYSICAL CONTROLS")
    c1, c2, c3 = st.columns(3)
    c1.toggle("OFFICE LIGHTS", value=True)
    c2.toggle("PERIMETER LOCKS", value=True)
    c3.toggle("AC SYSTEM (72°F)", value=True)

with tab3:
    st.subheader("SURVIVAL TELEMETRY")
    st.line_chart({"Battery": [80, 85, 90, 95, 100, 98, 97], "Water": [50, 50, 50, 60, 70, 70, 65]})
    st.error("OFFLINE ARK: DISCONNECTED (Air Gap Active)")
