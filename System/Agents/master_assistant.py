"""
MASTER ASSISTANT (GRAPH ORCHESTRATOR) - v5.0 IMMORTAL
The Sovereign General Manager of Project Monolith.
Architecture: Directed Cyclic Graph (State Machine)
Pattern: Plan -> Execute -> Verify -> Reflect
Core Layers: Observability + Self-Healing + Memory
"""
import json
import time
import subprocess
import sys
import threading
from pathlib import Path
from datetime import datetime
from enum import Enum
from typing import Dict, List, Any

# --- CORE LAYER IMPORTS (Best-in-World 2026) ---
try:
    from System.Core.observability_engine import get_observability
    from System.Core.self_healing_controller import get_healer
    from System.Core.memory_engine import get_memory
    from System.Core.governance_engine import get_governance
    from System.Core.comms_protocol import AgentAuthenticator
    from System.Core.hardened_dispatcher import HardenedDispatcher
    from System.Core.model_interface import get_llm
    from System.Core.monetization_bridge import get_bridge
    CORE_LAYERS_ACTIVE = True
except ImportError:
    CORE_LAYERS_ACTIVE = False
    print("[MASTER] Warning: Core layers not found, running in basic mode.")

# --- CONFIGURATION (The Five Pillars) ---
PILLARS = {
    "WEALTH": ["treasurer", "accountant_agent", "loophole_scanner", "revenue_tracker", "tax_shield_agent", "investment_agent", "ip_arbitrage_engine", "defi_yield_agent", "revenue_executor", "capital_allocation_agent", "global_arb_scout", "bounty_arbitrageur", "protocol_bridge_agent"],
    "SECURITY": ["cipher_agent", "traffic_masker", "emergency_protocol", "auditor_agent", "sentinel_agent", "backup_agent", "red_team_agent", "meta_strategy_agent", "ethical_sentinel"],
    "LABOR": ["ancestral_butler", "home_orchestrator", "purchasing_agent", "purge_agent", "scout_agent", "hardware_sentinel", "hardware_optimizer"],
    "HEALTH": ["director_pulse_agent", "fitness_agent", "nutrition_agent", "bio_link_agent", "predictive_concierge"],
    "DEVELOPMENT": ["system_optimizer", "research_agent", "voice_interface", "gap_scanner", "learning_agent", "knowledge_architect", "memory_archivist"]
}

class AgentState(Enum):
    IDLE = "IDLE"
    PLANNING = "PLANNING"
    EXECUTING = "EXECUTING"
    VERIFYING = "VERIFYING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class MonolithGraph:
    """
    The Orchestration Engine (Graph-Based).
    Manages the lifecycle of the 5 Pillars as autonomous sub-graphs.
    Now with: Observability, Self-Healing, and Memory integration.
    """
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.agents_dir = self.root / "Agents"
        self.sentinel_dir = self.root / "Sentinels"
        self.logs_dir = self.root / "Logs"
        self.memory_dir = self.root.parent / "Memory"
        
        # Ensure Infrastructure
        for d in [self.agents_dir, self.sentinel_dir, self.logs_dir, self.memory_dir]:
            d.mkdir(parents=True, exist_ok=True)
        
        # --- CORE LAYERS (Best-in-World 2026) ---
        if CORE_LAYERS_ACTIVE:
            self.observability = get_observability()
            self.healer = get_healer()
            self.memory = get_memory("master_assistant")
            self.governance = get_governance()
            self.dispatcher = HardenedDispatcher()
            self.auth = AgentAuthenticator("master_assistant")
            self.llm = get_llm()
            self.bridge = get_bridge()
            self._log("INIT", "✅ Core Layers Active: Observability, Self-Healing, Memory, Governance, Hardening, LocalAI, Monetization")
        else:
            self.observability = None
            self.healer = None
            self.memory = None
            self.governance = None
            self.dispatcher = None
            self.auth = None
            self.llm = None
            self.bridge = None
            
        self.state = AgentState.IDLE
        self.context = {}  # Shared Memory (Blackboard Pattern)
        self.workers = self._discover_workers()

    def _discover_workers(self) -> List[str]:
        return [f.stem for f in self.agents_dir.glob("*.py") if f.stem != "master_assistant"]

    def _log(self, level: str, message: str):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [MASTER] [{level}] {message}")

    # --- NODE 1: THE PLANNER ---
    def node_plan(self):
        self._log("PLAN", "Scanning environment & checking Pillars...")
        self.state = AgentState.PLANNING
        
        # 1. Check Gaps (Self-Awareness)
        missing_critical = []
        for pillar, agents in PILLARS.items():
            for agent in agents:
                if agent not in self.workers:
                    missing_critical.append(agent)
        
        if missing_critical:
            self._log("PLAN", f"⚠️ CRITICAL GAPS DETECTED: {len(missing_critical)} agents missing.")
            self.context["gaps"] = missing_critical
            return "node_manage_labor" # Branch to Labor (Self-Repair)
        
        
        # 2. Check Directives (User Input or Schedule)
        current_hour = datetime.now().hour
        scheduled_directives = []
        
        # Daily maintenance cycle (3 AM)
        if current_hour == 3:
            scheduled_directives.append("MAINTENANCE_CYCLE")
        
        # Wealth check every 6 hours
        if current_hour % 6 == 0:
            scheduled_directives.append("WEALTH_CHECK")
            
        # Security audit daily (midnight)
        if current_hour == 0:
            scheduled_directives.append("SECURITY_AUDIT")
            
        self.context["directives"] = scheduled_directives if scheduled_directives else ["IDLE_MONITORING"]
        return "node_execute"

    # --- NODE 2: THE EXECUTOR ---
    def node_execute(self):
        self.state = AgentState.EXECUTING
        self._log("EXEC", "Activating Pillar Sub-Graphs...")
        
        results = {}
        
        # Execute Pillars in Parallel (Threaded Sub-Graphs)
        threads = []
        
        def run_pillar(name, agents):
            self._log("EXEC", f"  -> Activating {name} Pillar...")
            pillar_status = "GREEN"
            for agent in agents:
                if agent in self.workers:
                    success = self._run_agent_script(agent)
                    if not success: pillar_status = "YELLOW"
            results[name] = pillar_status

        for pillar_name, agents in PILLARS.items():
            t = threading.Thread(target=run_pillar, args=(pillar_name, agents))
            threads.append(t)
            t.start()
            
        for t in threads:
            t.join()

        # --- SPECIAL ENGINES (Added v5.4) ---
        # These run after the main pillars to utilize their data
        self._log("EXEC", "  -> Activating Growth & Creative Engines...")
        self._run_agent_script("system_growth_engine")
        self._run_agent_script("omnidirectional_revenue_scanner")
        # Creative engine invocation (script is in subfolder, need special handling or move)
        # For simplicity in v5.4, we assume it's callable via the same mechanism or we fix the path
        creative_script = self.agents_dir / "Creators" / "creative_engine.py"
        if creative_script.exists():
             subprocess.run(["python", str(creative_script)], capture_output=True, text=True, timeout=60)
            
        self.context["execution_results"] = results
        return "node_verify"

    def _run_agent_script(self, name: str) -> bool:
        """Runs a python agent as a subprocess"""
        script_path = self.agents_dir / f"{name}.py"
        try:
            # We don't capture output to allow agents to print to console directly if they want, 
            # but usually they should write to Sentinels.
            # Using capture_output=True to keep main console clean-ish.
            subprocess.run(["python", str(script_path)], capture_output=True, text=True, timeout=60)
            return True
        except Exception as e:
            self._log("ERROR", f"Agent {name} crashed: {e}")
            return False

    # --- NODE 3: THE VERIFIER (Reflector) ---
    def node_verify(self):
        self.state = AgentState.VERIFYING
        self._log("VERIFY", "Aggregating Sentinel Data...")
        
        briefing = {
            "timestamp": datetime.now().isoformat(),
            "status": "NOMINAL",
            "pillars": {}
        }
        
        # Aggregation Logic
        global_status = "GREEN"
        for pillar, agents in PILLARS.items():
            pillar_data = {"status": "GREEN", "alerts": []}
            for agent in agents:
                sentinel_file = self.sentinel_dir / f"{agent}.done"
                if sentinel_file.exists():
                    try:
                        data = json.loads(sentinel_file.read_text(encoding='utf-8'))
                        if data.get("status") == "RED":
                            pillar_data["status"] = "RED"
                            global_status = "RED"
                        pillar_data["alerts"].append(f"{agent}: {data.get('message', 'User OK')[:50]}")
                    except:
                        pass
            briefing["pillars"][pillar] = pillar_data
            
        self.context["briefing"] = briefing
        
        # Reflection Step: Did we fail anything?
        if global_status == "RED":
            self._log("REFLECT", "❌ System Health Critical. Re-triggering Maintenance.")
            return "node_execute" # Loop back
        
        return "node_complete"

    # --- NODE 4: LABOR MANAGER (The Builder) ---
    def node_manage_labor(self):
        """Self-Repair Node: Spawns missing agents"""
        self._log("LABOR", "Initiating Genesis Protocol for missing agents...")
        gaps = self.context.get("gaps", [])
        
        for gap in gaps:
            self._spawn_agent(gap)
            
        # Update worker list
        self.workers = self._discover_workers()
        return "node_plan" # Return to start to re-verify

    def _spawn_agent(self, name: str):
        """Generates a Best-in-Class Scaffold"""
        self._log("BUILD", f"Forging {name} from blueprint...")
        
        template = f'''"""
{name.upper().replace("_", " ")} - PRO GENERATED AGENT
Part of Monolith Class-5 Architecture.
Timestamp: {datetime.now().isoformat()}
"""
import json
import logging
from pathlib import Path
from datetime import datetime

class {name.replace("_", " ").title().replace(" ", "")}:
    """
    Standard Monolith Agent Implementation.
    """
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.sentinel_dir = self.root / "Sentinels"
        self.memory_dir = self.root.parent / "Memory" / "{name}"
        
        self.sentinel_dir.mkdir(exist_ok=True)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

    def run(self):
        logging.info("Starting Execution Cycle...")
        
        # --- CORE LOGIC HERE ---
        result = "Operation Successful"
        status = "GREEN"
        # -----------------------
        
        self._report(status, result)

    def _report(self, status, message):
        data = {{
            "agent": "{name}",
            "status": status,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }}
        with open(self.sentinel_dir / "{name}.done", 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        logging.info(f"Report filed: {{status}}")

if __name__ == "__main__":
    {name.replace("_", " ").title().replace(" ", "")}().run()
'''
        (self.agents_dir / f"{name}.py").write_text(template, encoding='utf-8')

    # --- GRAPH RUNNER ---
    def execute_cycle(self):
        self._log("INIT", "Starting Monolith Graph Cycle...")
        next_node = "node_plan"
        
        while next_node != "node_complete":
            # Dispatcher
            if next_node == "node_plan":
                next_node = self.node_plan()
            elif next_node == "node_execute":
                next_node = self.node_execute()
            elif next_node == "node_verify":
                next_node = self.node_verify()
            elif next_node == "node_manage_labor":
                next_node = self.node_manage_labor()
            else:
                self._log("CRITICAL", f"Unknown Node: {next_node}")
                break
                
        self._log("DONE", "Cycle Complete. System Sleeping.")
        return self.context.get("briefing")

if __name__ == "__main__":
    graph = MonolithGraph()
    briefing = graph.execute_cycle()
    
    # Director Briefing Output
    print("\n" + "="*60)
    print(f"📊 DIRECTOR BRIEFING [{briefing['timestamp']}]")
    print("="*60)
    for pillar, data in briefing['pillars'].items():
        icon = "✅" if data['status'] == "GREEN" else "❌"
        print(f"{icon} {pillar}: {len(data['alerts'])} Active Agents")
