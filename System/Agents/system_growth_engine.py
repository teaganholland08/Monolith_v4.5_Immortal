"""
SYSTEM GROWTH ENGINE - Project Monolith v5.3
Purpose: The "Brain" of Capital Allocation & Self-Scaling.
Logic: Reinvest Earnings -> Upgrade Capabilities -> Scale Revenue
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

class SystemGrowthEngine:
    """
    Manages the 'Zero to Infinity' growth loop.
    Decides when to reinvest, when to upgrade hardware, and when to scale efforts.
    """
    
    def __init__(self):
        self.sentinel_dir = Path(__file__).parent.parent / "Sentinels"
        self.logs_dir = Path(__file__).parent.parent / "Logs" / "Treasury"
        self.sentinel_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True, parents=True)
        
        # Load the revenue scanner results
        self.scanner_file = self.sentinel_dir / "omnidirectional_revenue_scanner.done"
        
        # Growth thresholds (Capital Requirements)
        self.milestones = {
            "STAGE_1_SEED": 100.0,      # Upgrade to paid tools
            "STAGE_2_VELOCITY": 1000.0, # Outsource/Ads/Cloud VPS
            "STAGE_3_MOMENTUM": 5000.0, # High-yield DeFi/Consulting
            "STAGE_4_EMPIRE": 20000.0   # Full Automation/Hiring
        }

    def get_total_capital(self) -> float:
        """Calculate total liquid capital from all logs"""
        total = 0.0
        # In a real run, this would sum up verified transaction logs.
        # For now, we simulate reading the ledger.
        ledger_path = self.logs_dir / "execution_log.jsonl"
        if ledger_path.exists():
            with open(ledger_path, 'r') as f:
                for line in f:
                    try:
                        record = json.loads(line)
                        if record.get("action") == "REVENUE_INCOME":
                            total += float(record.get("amount", 0))
                        elif record.get("action") == "EXPENSE_REINVEST":
                            total -= float(record.get("amount", 0))
                    except:
                        pass
        return total

    def get_active_opportunities(self) -> List[Dict]:
        """Read what the scanner found"""
        if not self.scanner_file.exists():
            return []
        
        with open(self.scanner_file, 'r') as f:
            data = json.load(f)
            return data.get("revenue_streams", {})

    def decide_next_move(self, current_capital: float) -> Dict:
        """The Core Logic: Reinvest or Save?"""
        
        status = "MAINTAIN"
        action = "CONTINUE_GRIND"
        upgrade_target = None
        
        if current_capital < self.milestones["STAGE_1_SEED"]:
            status = "GRIND_MODE"
            action = "Focus on Time-for-Money (Microtasks, Content creation)"
            focus_area = "Micro-tasks & Bandwidth"
            
        elif current_capital >= self.milestones["STAGE_1_SEED"] and current_capital < self.milestones["STAGE_2_VELOCITY"]:
            status = "SEED_CAPITAL_ACQUIRED"
            action = "UPGRADE: Purchase Midjourney/Suno subscriptions to 10x output"
            upgrade_target = "Paid AI Tools"
            focus_area = "Digital Products (High Volume)"
            
        elif current_capital >= self.milestones["STAGE_2_VELOCITY"] and current_capital < self.milestones["STAGE_3_MOMENTUM"]:
            status = "VELOCITY_MODE"
            action = "SCALE: Migrate to Oracle Cloud VPS + Hire VA for administration"
            upgrade_target = "Cloud Infrastructure + VA"
            focus_area = "Agency Services & Automation"
            
        else:
            status = "EMPIRE_MODE"
            action = "DOMINATE: Maximize DeFi yields, acquisition channels, and paid ads"
            upgrade_target = "Business Acquisition / Ad Scale"
            focus_area = "Capital Deployment"
            
        return {
            "status": status,
            "recommended_action": action,
            "upgrade_target": upgrade_target,
            "focus_area": focus_area,
            "capital": current_capital
        }

    def run(self):
        print("[GROWTH-ENGINE] 🧠 Analyzing Economic State...")
        
        current_capital = self.get_total_capital()
        # For simulation/demo purposes if log is empty, let's assume we started (or user can input)
        # current_capital = 0.0 # Default
        
        opportunities = self.get_active_opportunities()
        decision = self.decide_next_move(current_capital)
        
        sentinel_data = {
            "agent": "system_growth_engine",
            "timestamp": datetime.now().isoformat(),
            "capital_state": current_capital,
            "growth_stage": decision["status"],
            "directive": decision["recommended_action"],
            "focus": decision["focus_area"]
        }
        
        # Write directive for Master Assistant
        with open(self.sentinel_dir / "system_growth_engine.done", 'w', encoding='utf-8') as f:
            json.dump(sentinel_data, f, indent=2)
            
        print(f"[GROWTH-ENGINE] 💰 Current Verified Capital: ${current_capital}")
        print(f"[GROWTH-ENGINE] 🚦 Stage: {decision['status']}")
        print(f"[GROWTH-ENGINE] 👉 Directive: {decision['recommended_action']}")
        
        return sentinel_data

if __name__ == "__main__":
    engine = SystemGrowthEngine()
    engine.run()
