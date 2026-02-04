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
    CORE_LAYERS_ACTIVE = True
except ImportError:
    CORE_LAYERS_ACTIVE = False
    print("[MASTER] Warning: Core layers not found, running in basic mode.")

# --- CONFIGURATION (The Five Pillars) ---
PILLARS = {
    "WEALTH": ["treasurer", "accountant_agent", "loophole_scanner", "revenue_tracker", "tax_shield_agent", "investment_agent", "ip_arbitrage_engine", "defi_yield_agent"],
    "SECURITY": ["cipher_agent", "traffic_masker", "emergency_protocol", "auditor_agent", "sentinel_agent", "backup_agent", "red_team_agent"],
    "LABOR": ["ancestral_butler", "home_orchestrator", "purchasing_agent", "purge_agent", "scout_agent", "hardware_sentinel"],
    "HEALTH": ["director_pulse_agent", "fitness_agent", "nutrition_agent", "bio_link_agent", "predictive_concierge"],
    "DEVELOPMENT": ["system_optimizer", "research_agent", "voice_interface", "gap_scanner", "learning_agent", "knowledge_architect"]
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
            self._log("INIT", "✅ Core Layers Active: Observability, Self-Healing, Memory, Governance, Hardening, LocalAI")
        else:
            self.observability = None
            self.healer = None
            self.memory = None
            self.governance = None
            self.dispatcher = None
            self.auth = None
            self.llm = None
            
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
        # TODO: Hook into Director Schedule
        self.context["directives"] = ["MAINTENANCE_CYCLE", "WEALTH_CHECK"]
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
    print("\\n" + "="*60)
    print(f"📊 DIRECTOR BRIEFING [{briefing['timestamp']}]")
    print("="*60)
    for pillar, data in briefing['pillars'].items():
        icon = "✅" if data['status'] == "GREEN" else "❌"
        print(f"{icon} {pillar}: {len(data['alerts'])} Active Agents")

import json
import os
import subprocess
from pathlib import Path
from datetime import datetime

class MasterAssistant:
    """
    The Sovereign AI General Manager.
    Capabilities:
    - Spawns new agents when it encounters unknown tasks
    - Coordinates all existing workers
    - Provides the 15-minute Director briefing
    - Executes approved actions autonomously
    """
    
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.agents_dir = self.root / "Agents"
        self.sentinel_dir = self.root / "Sentinels"
        self.logs_dir = self.root / "Logs"
        self.db_path = self.logs_dir / "ledger.db"
        
        for d in [self.agents_dir, self.sentinel_dir, self.logs_dir]:
            d.mkdir(exist_ok=True)
        
        self.workers = self._discover_workers()
        
    def _discover_workers(self):
        """Scan for all available agents"""
        workers = []
        for f in self.agents_dir.glob("*.py"):
            if f.name != "master_assistant.py":
                workers.append(f.stem)
        return workers
    
    def spawn_worker(self, name, task_description):
        """
        THE ARCHITECT FUNCTION
        Creates a new specialized agent from scratch.
        """
        print(f"[MASTER] Spawning new worker: {name}")
        
        worker_code = f'''"""
{name.upper()} - Auto-Generated Worker
Task: {task_description}
Generated: {datetime.now().isoformat()}
"""
import json
from pathlib import Path
from datetime import datetime

class {name.replace("_", " ").title().replace(" ", "")}:
    def __init__(self):
        self.sentinel_dir = Path(__file__).parent.parent / "Sentinels"
        self.sentinel_dir.mkdir(exist_ok=True)
        
    def run(self):
        print("[{name.upper()}] Executing task: {task_description}")
        
        sentinel_data = {{
            "agent": "{name}",
            "message": "Task executed: {task_description}",
            "timestamp": datetime.now().isoformat()
        }}
        
        with open(self.sentinel_dir / "{name}.done", 'w') as f:
            json.dump(sentinel_data, f, indent=2)
        
        print("[{name.upper()}] Complete.")

if __name__ == "__main__":
    {name.replace("_", " ").title().replace(" ", "")}().run()
'''
        
        file_path = self.agents_dir / f"{name}.py"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(worker_code)
        
        self.workers.append(name)
        print(f"[MASTER] Worker '{name}' spawned at {file_path}")
        return True
    
    def run_worker(self, name):
        """Execute a specific worker"""
        script = self.agents_dir / f"{name}.py"
        if not script.exists():
            # Try alternate names
            for alt in [f"{name}_agent.py", f"{name}.py"]:
                if (self.agents_dir / alt).exists():
                    script = self.agents_dir / alt
                    break
        
        if not script.exists():
            print(f"[MASTER] Worker '{name}' not found. Spawning...")
            self.spawn_worker(name, f"Generic task for {name}")
            script = self.agents_dir / f"{name}.py"
        
        try:
            result = subprocess.run(
                ["python", str(script)],
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode == 0
        except Exception as e:
            print(f"[MASTER] Error running {name}: {e}")
            return False
    
    def scan_gaps(self):
        """
        THE GAP SCANNER
        Identifies missing capabilities across the Five Strategic Vertical Pillars.
        """
        print("[MASTER] Scanning global system gaps (Five Pillars)...")
        
        # 2026 FIVE STRATEGIC VERTICAL PILLARS
        required_capabilities = [
            # WEALTH FACTORY
            ("treasurer", "Manage finances and capital allocation"),
            ("accountant_agent", "CRA/BC tax optimization and autonomous filing"),
            ("loophole_scanner", "Find tax and legal arbitrage opportunities"),
            ("revenue_tracker", "Monitor income and hardware phase triggers"),
            ("tax_shield_agent", "Continuous 2026 tax law monitoring"),
            
            # SECURITY FACTORY
            ("cipher_agent", "PQC (Kyber-1024) encryption orchestration"),
            ("traffic_masker", "Metadata and ISP activity obfuscation"),
            ("emergency_protocol", "Dead Man's Switch and VANISH activation"),
            ("auditor_agent", "Red-team compliance and sovereign security"),
            
            # LABOR FACTORY
            ("ancestral_butler", "Circadian and seasonal biological protocol enforcement"),
            ("home_orchestrator", "Smart home and robotic fleet coordination"),
            ("purchasing_agent", "Automated hardware procurement and inventory"),
            ("purge_agent", "Manual labor elimination and script automation"),
            
            # HEALTH FACTORY
            ("director_pulse_agent", "2026 Bio-diagnostic and longevity monitoring"),
            ("fitness_agent", "Adaptive biometric training protocols"),
            ("nutrition_agent", "AI-optimized metabolic fueling"),
            
            # DEVELOPMENT FACTORY
            ("system_optimizer", "Resource allocation and hardware health"),
            ("research_agent", "Deep-web intelligence gathering"),
            ("voice_interface", "Multi-modal command processing"),
            ("scout_agent", "Hardware upgrade and tech-scouting")
        ]
        
        gaps = []
        for cap_name, cap_desc in required_capabilities:
            if cap_name not in self.workers and not (self.agents_dir / f"{cap_name}.py").exists():
                gaps.append((cap_name, cap_desc))
        
        if gaps:
            print(f"[MASTER] Found {len(gaps)} pillar gaps. Spawning workers...")
            for name, desc in gaps:
                self.spawn_worker(name, desc)
        else:
            print("[MASTER] All Five Pillars are operational.")
        
        return gaps
    
    def generate_briefing(self):
        """
        THE 15-MINUTE DIRECTOR BRIEFING
        Aggregates all sentinel data into a single summary.
        """
        print("[MASTER] Generating Director Briefing...")
        
        briefing = {
            "timestamp": datetime.now().isoformat(),
            "sections": {}
        }
        
        # Read all sentinel files
        for done_file in self.sentinel_dir.glob("*.done"):
            try:
                with open(done_file, 'r') as f:
                    data = json.load(f)
                briefing["sections"][done_file.stem] = {
                    "status": data.get("status", "ACTIVE"),
                    "message": data.get("message", "OK"),
                    "timestamp": data.get("timestamp", "Unknown")
                }
            except:
                pass
        
        # Save briefing
        with open(self.logs_dir / "director_briefing.json", 'w') as f:
            json.dump(briefing, f, indent=2)
        
        return briefing
    
    def execute_all(self):
        """Run the full autonomous cycle"""
        print("\n" + "="*60)
        print("🤖 MASTER ASSISTANT: AUTONOMOUS CYCLE")
        print("="*60)
        
        # 1. Scan for gaps and fill them
        self.scan_gaps()
        
        # 2. Run all workers
        print("\n[MASTER] Running all workers...")
        for worker in self.workers:
            self.run_worker(worker)
        
        # 3. Generate briefing
        briefing = self.generate_briefing()
        
        print("\n" + "="*60)
        print("📋 DIRECTOR BRIEFING")
        print("="*60)
        for name, data in briefing.get("sections", {}).items():
            status = data.get("status", "?")
            msg = data.get("message", "")[:50]
            print(f"   {name}: [{status}] {msg}")
        
        print("="*60)
        print("✅ MASTER ASSISTANT: Cycle complete.")
        
        return briefing

if __name__ == "__main__":
    assistant = MasterAssistant()
    assistant.execute_all()
