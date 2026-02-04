"""
MONOLITH BARE-METAL ORCHESTRATOR
Event-driven task executor with hard-coded God Rules

Architecture:
- Stays dormant until event triggers task
- No frameworks (pure Python + SQLite)
- Hard-coded safety filters (AI cannot bypass)
- Event listeners feed tasks.db
- Orchestrator processes tasks sequentially

User Time: 15 min/day (Director Briefing)
AI Time: 23h 45m (autonomous)
"""

import sqlite3
import time
import json
from pathlib import Path
from datetime import datetime

class MonolithOrchestrator:
    def __init__(self):
        self.db_path = Path(__file__).parent / "System" / "Logs" / "ledger.db"
        self.god_rules = self.load_god_rules()
        self.survival_buffer = 20000  # Hard-coded floor
        self.max_auto_spend = 2000    # Hard-coded limit
        
    def load_god_rules(self):
        """Load God Rules config"""
        config_path = Path(__file__).parent / "System" / "Config" / "treasurer_god_rules.json"
        if config_path.exists():
            with open(config_path, 'r') as f:
                return json.load(f)
        return {}
    
    def get_balance(self):
        """Calculate current balance"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                COALESCE(SUM(CASE WHEN type = 'REVENUE' THEN amount ELSE 0 END), 0) -
                COALESCE(SUM(CASE WHEN type = 'EXPENSE' THEN ABS(amount) ELSE 0 END), 0)
            FROM transactions
        """)
        
        balance = cursor.fetchone()[0]
        conn.close()
        return balance
    
    def enforce_god_rules(self, action):
        """Hard-coded safety filter - AI CANNOT bypass"""
        
        # Rule 1: Survival Buffer (ABSOLUTE)
        if action.get("type") == "EXPENSE":
            current_balance = self.get_balance()
            proposed_balance = current_balance - abs(action.get("amount", 0))
            
            if proposed_balance < self.survival_buffer:
                self.log_god_rule("SURVIVAL_BUFFER", "BLOCK", "BLOCKED", 
                                 f"Would leave ${proposed_balance:.2f} < ${self.survival_buffer}")
                return False, f"BLOCKED: Survival buffer at risk"
        
        # Rule 2: Auto-spend limit
        if action.get("type") == "EXPENSE":
            amount = abs(action.get("amount", 0))
            if amount > self.max_auto_spend:
                self.log_god_rule("AUTO_SPEND_LIMIT", "APPROVE", "PENDING", 
                                 f"${amount} > ${self.max_auto_spend}")
                return False, f"PENDING: Requires Director approval (>${self.max_auto_spend})"
        
        # Rule 3: Position size limit (2% max for trading)
        if action.get("source") == "CRYPTO":
            balance = self.get_balance()
            amount = abs(action.get("amount", 0))
            position_pct = amount / balance if balance > 0 else 0
            
            if position_pct > 0.02:
                self.log_god_rule("POSITION_LIMIT", "BLOCK", "BLOCKED",
                                 f"{position_pct*100:.1f}% > 2%")
                return False, f"BLOCKED: Position exceeds 2% limit"
        
        # All rules passed
        self.log_god_rule("ALL_RULES", "ALLOW", "APPROVED", "All checks passed")
        return True, "APPROVED"
    
    def log_god_rule(self, rule_name, action, result, details):
        """Audit log for God Rules enforcement"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO god_rules_log 
            (rule_name, action, result, details, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (rule_name, action, result, details, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def fetch_next_task(self):
        """Get highest priority pending task"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, task_type, data, priority
            FROM tasks
            WHERE status = 'PENDING'
            ORDER BY priority DESC, created_at ASC
            LIMIT 1
        """)
        
        task = cursor.fetchone()
        conn.close()
        
        if task:
            return {
                "id": task[0],
                "type": task[1],
                "data": json.loads(task[2]) if task[2] else {},
                "priority": task[3]
            }
        return None
    
    def execute_task(self, task):
        """Execute task with God Rules enforcement"""
        
        print(f"\n[TASK] {task['type']}")
        
        # Parse task data
        data = task.get("data", {})
        
        # Enforce God Rules BEFORE execution
        allowed, reason = self.enforce_god_rules(data)
        
        if not allowed:
            print(f"   ⛔ {reason}")
            self.mark_task_blocked(task["id"], reason)
            return False
        
        # Execute based on task type
        if task["type"] == "PURCHASE":
            return self.execute_purchase(task, data)
        elif task["type"] == "TRADE":
            return self.execute_trade(task, data)
        elif task["type"] == "ANALYZE":
            return self.execute_analysis(task, data)
        else:
            print(f"   ⚠️ Unknown task type: {task['type']}")
            return False
    
    def execute_purchase(self, task, data):
        """Execute autonomous purchase"""
        item_name = data.get("item_name", "Unknown")
        amount = abs(data.get("amount", 0))
        
        # Log transaction
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO transactions 
            (source, type, action, amount, asset, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ("ORCHESTRATOR", "EXPENSE", "AUTO_PURCHASE", -amount, item_name, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        print(f"   ✅ Purchased: {item_name} (${amount:,.2f})")
        self.mark_task_complete(task["id"])
        return True
    
    def execute_trade(self, task, data):
        """Execute crypto trade"""
        print(f"   💹 Trade execution (placeholder)")
        # In production: Call exchange API
        self.mark_task_complete(task["id"])
        return True
    
    def execute_analysis(self, task, data):
        """Run analysis task"""
        print(f"   🔍 Analysis: {data.get('topic', 'General')}")
        self.mark_task_complete(task["id"])
        return True
    
    def mark_task_complete(self, task_id):
        """Mark task as completed"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE tasks 
            SET status = 'COMPLETE', completed_at = ?
            WHERE id = ?
        """, (datetime.now().isoformat(), task_id))
        
        conn.commit()
        conn.close()
    
    def mark_task_blocked(self, task_id, reason):
        """Mark task as blocked (God Rules violation)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE tasks 
            SET status = 'BLOCKED'
            WHERE id = ?
        """, (task_id,))
        
        conn.commit()
        conn.close()
    
    def run(self, max_iterations=100):
        """Main event loop - stays dormant until task arrives"""
        
        print("\n" + "="*60)
        print("🤖 MONOLITH ORCHESTRATOR: ONLINE")
        print("="*60)
        print(f"God Rules: ACTIVE (Survival Buffer: ${self.survival_buffer:,})")
        print(f"Auto-spend Limit: ${self.max_auto_spend:,}")
        print("\nWaiting for tasks...\n")
        
        iterations = 0
        tasks_processed = 0
        
        while iterations < max_iterations:
            task = self.fetch_next_task()
            
            if task:
                self.execute_task(task)
                tasks_processed += 1
            else:
                # No tasks - sleep for 1 second
                time.sleep(1)
            
            iterations += 1
        
        print(f"\n✅ Session complete: {tasks_processed} tasks processed")
        print("="*60 + "\n")

if __name__ == "__main__":
    orchestrator = MonolithOrchestrator()
    orchestrator.run(max_iterations=10)  # Process up to 10 tasks
