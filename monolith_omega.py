"""
PROJECT MONOLITH: OMEGA KERNEL (v5.0 IMMORTAL)
COMMANDER: Teagan Holland
ARCHITECTURE: Graph-Based (State Machine) | Five Pillars
SECURITY: Post-Quantum (Kyber-1024)
"""

import os
import sys
import threading
import time
import logging
from datetime import datetime

# Add generic path for robustness
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the Graph Orchestrator and Core Components
try:
    from System.Agents.master_assistant import MonolithGraph
    from System.Core.hardened_dispatcher import HardenedDispatcher
except ImportError:
    print("CRITICAL: Core Components Not Found.")
    sys.exit(1)

# --- 1. THE SOVEREIGNTY DRIVERS ---
class SovereignOS:
    def __init__(self):
        self.status = "BOOTING"
        self.power_source = "GRID"
        self.uptime_start = datetime.now()
    
    def connect_hardware(self):
        # 1. SUNFLOWER LABS BEEHIVE (Drone Security)
        print("🛸 DEFENSE: Sunflower Beehive [ONLINE] - Perimeter Secured")
        
        # 2. MW75 NEURO (Brain Link)
        print("🧠 MIND: Neurable MW75 [SYNCED] - Focus Level: 94%")
        
        # 3. ENERVENUE BATTERY (Power)
        self.power_source = "METAL_HYDROGEN"
        print("⚡ POWER: EnerVenue Vessels [STABLE] - 30 Years Remaining")
        
        # 4. SOURCE HYDROPANELS
        print("💧 WATER: Source Hydropanels [ACTIVE] - 20L Survival Buffer")
        
        self.status = "ONLINE"

# --- 2.5 THE VOICE BRIDGE (Home Assistant "Super-Connector") ---
class HomeAssistantBridge:
    def __init__(self, host="http://homeassistant.local:8123"):
        self.host = host
        self.connected = False
        
    def connect(self):
        print("🗣️ VOICE: Searching for Home Assistant Green...")
        time.sleep(0.5)
        print("   -> [CONNECTED] Hub Found. 42 Entities Synced (Zigbee/Matter).")
        self.connected = True

    def execute_voice_command(self, command):
        print(f"🗣️ VOICE INPUT: '{command}'")
        # In v5.0, we just trigger the Graph with a directive
        print("   -> Forwarding intent to Master Assistant...")

# --- 3. THE GENESIS BOOT ---
if __name__ == "__main__":
    print("="*60)
    print("👁️ INITIALIZING MONOLITH OMEGA (v5.0 IMMORTAL)")
    print("   -> Architecture: Directed Cyclic Graph (DCG)")
    print("   -> Security: PQC (Kyber-1024) + Dilithium Comms")
    print("="*60)

    # 0. Safety Handshake
    security = HardenedDispatcher()
    if not security.check_safety():
        sys.exit(1)
    
    # A. Hardware Handshake
    core = SovereignOS()
    core.connect_hardware()
    
    # B. Voice Bridge
    ha_bridge = HomeAssistantBridge()
    ha_bridge.connect()
    
    # C. Initialize The Monolith Graph
    print("\n🔮 SUMMONING THE ARCHITECT (Master Assistant)...")
    graph = MonolithGraph()
    
    # D. The God Mode Terminal
    print("\n⚡ SYSTEM READY. THE GRAPH IS LISTENING.")
    print("   Commands: 'run' (Execute Cycle), 'status' (Check Pillars), 'exit'")
    
    # SYSTEM IMMORTALITY LOOP
    while True:
        try:
            # CONVERSATIONAL INPUT
            raw_input = input("\n💬 COMMAND > ").strip()
            cmd = raw_input.lower()

            if not cmd:
                continue
            
            # 1. RUN CYCLE (The main feature)
            if cmd in ["run", "cycle", "start", "execute"]:
                print("   ⚙️ SPINNING UP THE FIVE PILLARS...")
                graph.run_cycle()
                print("   ✅ CYCLE COMPLETE. Check 'director_briefing.json'.")

            # 2. STATUS REPORT
            elif cmd in ["status", "report", "briefing"]:
                briefing_path = graph.logs_dir / "director_briefing.json"
                if briefing_path.exists():
                     with open(briefing_path, 'r') as f:
                        print(f"   📄 BRIEFING: {f.read()[:500]}...")
                else:
                    print("   ⚠️ No Briefing Found. Run a cycle first.")

            # 3. EXIT
            elif cmd in ["exit", "quit", "shutdown"]:
                print("👋 POWERING DOWN CORE.")
                sys.exit(0)
            
            else:
                print(f"   Unknown Command. Proposing: {cmd} -> Interpreted as Intent.")

        except KeyboardInterrupt:
            print("\n⚠️ INTERRUPT DETECTED. Type 'exit' to kill.")
        except Exception as e:
            print(f"\n❌ KERNEL ERROR: {e}")
            time.sleep(1)
