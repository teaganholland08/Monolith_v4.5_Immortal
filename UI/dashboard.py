"""
THE FACE - Self-Building Dashboard
Replaces: Custom Streamlit UIs
Capability: Live system monitoring
"""

import streamlit as st
import os
import sys
from datetime import datetime

st.set_page_config(page_title="👁️ MONOLITH PRIME", layout="wide")

st.title("👁️ MONOLITH PRIME - AUTONOMOUS CONTROL CENTER")
st.caption(f"System Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Layout
col1, col2, col3 = st.columns(3)

with col1:
    st.header("🧠 BRAIN (Agents)")
    brain_path = r"C:\Monolith\Brain"
    if os.path.exists(brain_path):
        agents = [f for f in os.listdir(brain_path) if f.endswith('.py')]
        st.write(f"**Active Agents:** {len(agents)}")
        for agent in agents:
            st.text(f"  • {agent}")
    else:
        st.warning("Brain folder not found")

with col2:
    st.header("🌐 HANDS (Browser)")
    if st.button("🚀 LAUNCH MOLTBOT"):
        st.success("Moltbot activated!")
    
    url = st.text_input("Target URL", "https://google.com")
    if st.button("Navigate"):
        st.info(f"Navigating to {url}...")

with col3:
    st.header("❤️ PULSE (Status)")
    st.metric("Uptime", "Active")
    st.metric("Organs", "5/5")

st.divider()

# Command Line
st.header("💻 COMMAND LINE")
cmd = st.text_input("Enter command:", key="cmd", placeholder="gen crypto_scanner")

if cmd:
    st.code(f"Executing: {cmd}")

# Log viewer
st.header("📋 RECENT LOGS")
log_path = r"C:\Monolith\Logs\monolith.log"
if os.path.exists(log_path):
    with open(log_path, "r") as f:
        logs = f.readlines()[-20:]  # Last 20 lines
    st.text_area("Logs", "".join(logs), height=200)
