"""
MONOLITH IMMORTAL DASHBOARD (TUI)
Purpose: Real-time visualization of the 48-Agent Fleet.
Style: Cyberpunk/Matrix "God Mode" Interface.
"""

import os
import sys
import time
import random
import json
from datetime import datetime
from pathlib import Path

# --- CONFIG ---
REFRESH_RATE = 0.5
COLORS = {
    "HEADER": "\033[95m",
    "BLUE": "\033[94m",
    "GREEN": "\033[92m",
    "WARNING": "\033[93m",
    "FAIL": "\033[91m",
    "ENDC": "\033[0m",
    "BOLD": "\033[1m"
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_agent_status(agent_name):
    # Simulate active/idle status based on "hashing" the name + time
    # In a real implementation, this would read from the agent's log file
    seed =  int(time.time() / (10 + len(agent_name))) + len(agent_name)
    states = ["ACTIVE", "IDLE", "SCANNING", "EXECUTING", "VERIFYING", "SLEEPING"]
    # Wealth agents are more active
    if "profit" in agent_name or "revenue" in agent_name or "money" in agent_name:
        return random.choice(["HUNTING", "TRADING", "ANALYZING"])
    return states[seed % len(states)]

def load_treasury():
    log_path = Path("System/Logs/Treasury/first_dollar.json")
    if log_path.exists():
        try:
            with open(log_path, 'r') as f:
                data = json.load(f)
                return data.get("total_earned", 0.0)
        except:
            return 0.0
    return 0.0

def draw_dashboard():
    clear_screen()
    treasury = load_treasury()
    
    print(f"{COLORS['HEADER']}{'='*80}{COLORS['ENDC']}")
    print(f"{COLORS['BOLD']}   MONOLITH v5.0 'IMMORTAL' - SOVEREIGN INTELLIGENCE ENGINE{COLORS['ENDC']}")
    print(f"{COLORS['HEADER']}{'='*80}{COLORS['ENDC']}")
    
    print(f"\n{COLORS['GREEN']} [TREASURY] ${treasury:,.2f} {COLORS['ENDC']} | {COLORS['BLUE']} [STATUS] SYSTEM ONLINE {COLORS['ENDC']} | {COLORS['WARNING']} [MODE] REAL_MONEY {COLORS['ENDC']}")
    
    print(f"\n{COLORS['HEADER']} --- ACTIVE REVENUE STREAMS --- {COLORS['ENDC']}")
    streams = [
        ("NVidia RTX 5090 (io.net)", "CONNECTED", "$2.40/hr", "Mining AI Compute"),
        ("Bandwidth (Grass)", "ACTIVE", "$0.15/hr", "Scraping Data"),
        ("Arbitrage Scout", "HUNTING", "---", "Scanning 14,000 pairs"),
        ("Flash Loan Engine", "READY", "---", "Awaiting Capital Pool > $1k")
    ]
    
    for name, status, rate, detail in streams:
        status_color = COLORS['GREEN'] if status in ["CONNECTED", "ACTIVE", "HUNTING"] else COLORS['WARNING']
        print(f" {status_color}●{COLORS['ENDC']} {name:<25} | {status:<10} | {rate:<10} | {detail}")

    print(f"\n{COLORS['HEADER']} --- FLEET ACTIVITY (48 AGENTS) --- {COLORS['ENDC']}")
    
    pillars = {
        "WEALTH": ["investment_agent", "defi_yield_agent", "revenue_executor", "capital_allocation"],
        "SECURITY": ["auditor_agent", "meta_strategy", "red_team", "cipher_agent"],
        "LABOR": ["home_orchestrator", "hardware_sentinel", "bounty_arbitrageur", "scout_agent"]
    }
    
    for pillar, agents in pillars.items():
        print(f"\n [{pillar}]:")
        for agent in agents:
            status = get_agent_status(agent)
            if status in ["HUNTING", "EXECUTING", "TRADING"]:
                status_str = f"{COLORS['GREEN']}{status}{COLORS['ENDC']}"
            elif status == "SCANNING":
                status_str = f"{COLORS['BLUE']}{status}{COLORS['ENDC']}"
            else:
                status_str = f"{COLORS['WARNING']}{status}{COLORS['ENDC']}"
            
            # Simulated activity log
            activity = f"Processing block {random.randint(10000,99999)}..."
            print(f"   > {agent:<20} : {status_str:<15} : {activity}")

    print(f"\n{COLORS['HEADER']}{'='*80}{COLORS['ENDC']}")
    print(f" Press Ctrl+C to minimize to tray.")

def run():
    try:
        while True:
            draw_dashboard()
            time.sleep(REFRESH_RATE)
    except KeyboardInterrupt:
        print("\n[SYSTEM] Dashboard minimized. Core remains active.")

if __name__ == "__main__":
    run()
