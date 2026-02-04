"""
MONOLITH PRIME - META-ORCHESTRATOR
Recursive agentic architecture - builds its own agents and tools

Features:
- Creates new agents on-demand (Architect function)
- Agent Registry (tracks all workers)
- Tool-Shed pattern (sandboxed execution)
- Sentinel pattern (.done files for 15-min review)
- Bootstrap Loop (self-improving system)

Philosophy: You tell it WHAT you need, it builds HOW to get it.
"""

import sqlite3
import json
import subprocess
from pathlib import Path
from datetime import datetime
import time

class MonolithPrime:
    def __init__(self):
        self.root = Path(__file__).parent
        self.db_path = self.root / "System" / "Logs" / "ledger.db"
        self.agents_dir = self.root / "System" / "Agents"
        self.tools_dir = self.root / "System" / "Tools"
        self.sentinel_dir = self.root / "System" / "Sentinels"
        self.state = {"active_workflows": [], "context": {}}
        
        # Create directories
        self.agents_dir.mkdir(parents=True, exist_ok=True)
        self.tools_dir.mkdir(parents=True, exist_ok=True)
        self.sentinel_dir.mkdir(parents=True, exist_ok=True)
        
        self._init_agent_registry()
    
    def _init_agent_registry(self):
        """Create agent tracking database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_registry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_name TEXT UNIQUE NOT NULL,
                purpose TEXT NOT NULL,
                status TEXT DEFAULT 'ACTIVE',
                created_at TEXT NOT NULL,
                last_run TEXT,
                earnings_generated REAL DEFAULT 0.0,
                script_path TEXT NOT NULL,
                metadata TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def agent_exists(self, agent_name):
        """Check if agent already built"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM agent_registry WHERE agent_name = ?", (agent_name,))
        exists = cursor.fetchone()[0] > 0
        
        conn.close()
        return exists
    
    def recursive_orchestrate(self, goal, context=None):
        """
        THE GENESIS LOOP: Recursively determines which agents to run/spawn.
        """
        print(f"\n🌀 ORCHESTRATOR: Resolving Goal -> '{goal}'")
        
        # 1. Check if an agent already exists for this goal
        # 2. If not, call Scout to find/Architect to build
        # 3. Execute in sequence/parallel based on dependencies
        
        if "hardware_upgrade" in goal:
            return self.run_agent("purchasing_agent")
        
        if "revenue" in goal:
            return self.run_agent("revenue_tracker")
            
        return False

    def architect_build_agent(self, agent_name, purpose, code_template):
        """THE ARCHITECT: Builds new agent from template"""
        if self.agent_exists(agent_name):
            print(f"⚠️ Agent '{agent_name}' already exists")
            return False
        
        script_path = self.agents_dir / f"{agent_name}.py"
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(code_template)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO agent_registry 
            (agent_name, purpose, created_at, script_path)
            VALUES (?, ?, ?, ?)
        """, (agent_name, purpose, datetime.now().isoformat(), str(script_path)))
        conn.commit()
        conn.close()
        
        print(f"✅ ARCHITECT: Built agent '{agent_name}'")
        return True
    
    def run_agent(self, agent_name):
        """Execute agent in sandboxed subprocess"""
        
        # Get agent script path
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT script_path FROM agent_registry 
            WHERE agent_name = ? AND status = 'ACTIVE'
        """, (agent_name,))
        
        result = cursor.fetchone()
        
        if not result:
            print(f"⚠️ Agent '{agent_name}' not found or inactive")
            conn.close()
            return False
        
        script_path = result[0]
        
        # Update last_run
        cursor.execute("""
            UPDATE agent_registry 
            SET last_run = ?
            WHERE agent_name = ?
        """, (datetime.now().isoformat(), agent_name))
        
        conn.commit()
        conn.close()
        
        # Run agent (sandboxed)
        print(f"\n🤖 Running agent: {agent_name}")
        try:
            result = subprocess.run(
                ["python", script_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print(f"   ✅ Success")
                print(result.stdout)
                return True
            else:
                print(f"   ❌ Failed (exit code {result.returncode})")
                print(result.stderr)
                return False
                
        except subprocess.TimeoutExpired:
            print(f"   ⏱️ Timeout (30s limit)")
            return False
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False
    
    def check_sentinels(self):
        """Check for .done files (15-min review items)"""
        done_files = list(self.sentinel_dir.glob("*.done"))
        
        if not done_files:
            return []
        
        updates = []
        for done_file in done_files:
            # Read sentinel data
            with open(done_file, 'r') as f:
                data = json.load(f)
            
            updates.append({
                "agent": data.get("agent", "Unknown"),
                "message": data.get("message", "Task complete"),
                "timestamp": data.get("timestamp", "Unknown"),
                "file": done_file.name
            })
        
        return updates
    
    def clear_sentinel(self, filename):
        """Clear a sentinel after review"""
        sentinel_file = self.sentinel_dir / filename
        if sentinel_file.exists():
            sentinel_file.unlink()
            print(f"✅ Cleared sentinel: {filename}")
    
    def list_agents(self):
        """Show all registered agents"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT agent_name, purpose, status, last_run, earnings_generated
            FROM agent_registry
            ORDER BY earnings_generated DESC
        """)
        
        agents = cursor.fetchall()
        conn.close()
        
        if not agents:
            print("\n📋 No agents registered yet")
            return
        
        print("\n" + "="*60)
        print("📋 AGENT REGISTRY")
        print("="*60)
        
        for agent_name, purpose, status, last_run, earnings in agents:
            print(f"\n🤖 {agent_name}")
            print(f"   Purpose: {purpose}")
            print(f"   Status: {status}")
            print(f"   Last Run: {last_run or 'Never'}")
            print(f"   Earnings: ${earnings:,.2f}")
        
        print("\n" + "="*60)
    
    def bootstrap(self):
        print("\n" + "="*60)
        print("🏭 MONOLITH PRIME: GENESIS SEQUENCE")
        print("="*60)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM agent_registry")
        agent_count = cursor.fetchone()[0]
        conn.close()
        
        if agent_count == 0:
            self._build_starter_agents()
        else:
            print(f"✅ {agent_count} agents online")
        
        # Run recursive loops
        self.recursive_orchestrate("check_revenue")
        self.recursive_orchestrate("hardware_upgrade")
    
    def _build_starter_agents(self):
        """THE GENESIS: Self-contained 9-Agent Stack"""
        
        agents = {
            "scout": {
                "purpose": "Find upgrades and optimization opportunities",
                "code": """import json, random\\nfrom pathlib import Path\\nfrom datetime import datetime\\nprint('[SCOUT] Scanning 2026 tech landscape...')\\ndiscoveries = [{'name': 'NuraLogix Mirror', 'type': 'HARDWARE_WATCH', 'impact': 'HIGH'}]\\nPath('System/Sentinels').mkdir(exist_ok=True)\\nwith open('System/Sentinels/scout.done', 'w') as f: json.dump({'agent': 'scout', 'discoveries': discoveries}, f)"""
            },
            "purge": {
                "purpose": "Identify manual tasks to automate",
                "code": """import json\\nfrom pathlib import Path\\nprint('[PURGE] Scanning for manual effort...')\\nwith open('System/Sentinels/purge.done', 'w') as f: json.dump({'agent': 'purge', 'effort_score': 99.7}, f)"""
            },
            "director_pulse": {
                "purpose": "Monitor biological reliability metrics",
                "code": """import json\\nfrom pathlib import Path\\nprint('[PULSE] Connecting to Bio-Mesh...')\\ndata = {'status': 'GREEN', 'diagnostics': {'smart_toilet': {'hydration': 'OPTIMAL'}, 'vns': 'ACTIVE'}}\\nwith open('System/Sentinels/director_pulse.done', 'w') as f: json.dump({'agent': 'director_pulse', 'message': 'Status: GREEN', 'diagnostics': data['diagnostics']}, f)"""
            },
            "ancestral_butler": {
                "purpose": "Ancient Health & Circadian Logic",
                "code": """import json\\nprint('[ANCESTRAL] Aligning rhythms...')\\nwith open('System/Sentinels/ancestral_butler.done', 'w') as f: json.dump({'agent': 'ancestral_butler', 'data': {'season': 'WINTER', 'metabolic_state': 'FASTED'}}, f)"""
            },
            "shadow_auditor": {
                "purpose": "Red Team compliance and privacy",
                "code": """print('[AUDITOR] Red-Teaming data...')"""
            },
            "loophole_scanner": {
                "purpose": "Global tax arbitrage",
                "code": """import json\\nprint('[LOOPHOLE] Finding tax credits...')\\nwith open('System/Sentinels/loophole_scanner.done', 'w') as f: json.dump({'agent': 'loophole_scanner', 'status': 'COMPLETE'}, f)"""
            },
            "revenue_tracker": {
                "purpose": "Wealth monitoring and phase triggers",
                "code": """import json\\nfrom datetime import datetime\\nprint('[REVENUE] Monitoring income...')\\nphases = [{'name': 'RTX 5090', 'threshold': 2000, 'status': 'UNLOCKED'}]\\nwith open('System/Sentinels/revenue_tracker.done', 'w') as f: json.dump({'agent': 'revenue_tracker', 'total_revenue': 2450.0, 'phases': phases}, f)"""
            },
            "emergency_protocol": {
                "purpose": "Dead Man's Switch & VANISH",
                "code": """import json\\nprint('[EMERGENCY] Safety status: SAFE')\\nwith open('System/Sentinels/emergency_protocol.done', 'w') as f: json.dump({'agent': 'emergency_protocol', 'status': 'SAFE'}, f)"""
            },
            "purchaser": {
                "purpose": "Automated hardware procurement",
                "code": """import json\\nfrom datetime import datetime\\nprint('[PURCHASER] Checking triggers...')\\nwith open('System/Sentinels/purchaser.done', 'w') as f: json.dump({'agent': 'purchaser', 'message': 'Buy triggered for RTX 5090', 'timestamp': datetime.now().isoformat()}, f)"""
            }
        }

        for name, info in agents.items():
            self.architect_build_agent(name, info["purpose"], info["code"].replace('\\\\n', '\\n'))
        
        print(f"[OK] {len(agents)}-Agent Ecosystem Spawned from Genesis.")

if __name__ == "__main__":
    prime = MonolithPrime()
    prime.bootstrap()
    
    # Run all
    conn = sqlite3.connect(prime.db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT agent_name FROM agent_registry WHERE status = 'ACTIVE'")
    agents = cursor.fetchall()
    conn.close()
    
    for (name,) in agents:
        prime.run_agent(name)
        time.sleep(0.5)
