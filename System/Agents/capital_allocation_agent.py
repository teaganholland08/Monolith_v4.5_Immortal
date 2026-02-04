"""
CAPITAL ALLOCATION AGENT - Project Monolith v5.0
Purpose: Recursive Revenue Scaling Engine
Strategy: Use earnings from low-yield sources to unlock high-yield sources.

REVENUE LADDER:
$0 → DePIN ($60/day) 
→ $100 → CEX Swing Trading ($5-20/day)
→ $1000 → Flash Loan Arbitrage ($50-500/day)
→ $10,000 → Liquidity Provision ($100-1000/day)
→ $100,000 → Algorithmic Market Making (unlimited)
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

class RevenueStage:
    """Defines a revenue opportunity and its capital requirement"""
    def __init__(self, name: str, min_capital: float, daily_yield: tuple, risk: str):
        self.name = name
        self.min_capital = min_capital
        self.daily_yield = daily_yield  # (min, max)
        self.risk = risk
        self.unlocked = False

class CapitalAllocationAgent:
    """
    The Economic Optimization Engine.
    Automatically reallocates capital to maximize ROI.
    """
    
    def __init__(self):
        self.sentinel_dir = Path(__file__).parent.parent / "Sentinels"
        self.sentinel_dir.mkdir(exist_ok=True)
        
        # Define the Revenue Ladder
        self.stages = [
            RevenueStage("DePIN_GPU", 0, (40, 80), "NONE"),
            RevenueStage("DePIN_Bandwidth", 0, (1, 3), "NONE"),
            RevenueStage("IP_Arbitrage", 0, (10, 100), "LOW"),
            RevenueStage("CEX_Swing_Trade", 100, (5, 20), "MEDIUM"),
            RevenueStage("Flash_Loan_Arb", 1000, (50, 500), "MEDIUM"),
            RevenueStage("Liquidity_Provider", 10000, (100, 1000), "HIGH"),
            RevenueStage("Market_Making", 100000, (500, 5000), "EXPERT")
        ]
        
        self.current_capital = 0.0
        self.daily_revenue = 0.0
        
    def check_unlockable_stages(self) -> List[RevenueStage]:
        """Check which stages can be unlocked with current capital"""
        unlockable = []
        for stage in self.stages:
            if not stage.unlocked and self.current_capital >= stage.min_capital:
                unlockable.append(stage)
        return unlockable
    
    def allocate_capital(self, new_earnings: float) -> Dict:
        """
        Core Reinvestment Logic:
        1. Add new earnings to capital pool
        2. Check for unlockable stages
        3. Allocate capital to highest-yield stage
        """
        self.current_capital += new_earnings
        print(f"[CAPITAL] 💰 Total Capital: ${self.current_capital:.2f}")
        
        unlockable = self.check_unlockable_stages()
        allocations = []
        
        for stage in unlockable:
            if stage.min_capital <= self.current_capital:
                allocation_amount = stage.min_capital
                stage.unlocked = True
                self.current_capital -= allocation_amount
                
                allocations.append({
                    "stage": stage.name,
                    "allocated": allocation_amount,
                    "expected_daily": f"${stage.daily_yield[0]}-{stage.daily_yield[1]}",
                    "status": "UNLOCKED"
                })
                
                print(f"[CAPITAL] 🚀 UNLOCKED: {stage.name} (${allocation_amount} allocated)")
        
        return {
            "new_earnings": new_earnings,
            "capital_remaining": self.current_capital,
            "allocations": allocations,
            "stages_unlocked": len(allocations)
        }
    
    def get_revenue_projection(self) -> Dict:
        """Calculate projected revenue from all unlocked stages"""
        daily_min = 0
        daily_max = 0
        
        for stage in self.stages:
            if stage.unlocked:
                daily_min += stage.daily_yield[0]
                daily_max += stage.daily_yield[1]
        
        return {
            "daily_range": (daily_min, daily_max),
            "monthly_range": (daily_min * 30, daily_max * 30),
            "annual_range": (daily_min * 365, daily_max * 365)
        }
    
    def run(self):
        """
        Simulation: Process earnings from other agents and allocate
        """
        print("[CAPITAL] 💼 Running Capital Allocation Cycle...")
        
        # Simulate checking treasury for new earnings
        # In production, this reads from System/Logs/Treasury/execution_log.jsonl
        simulated_earnings = 150.00  # Example: $150 from first week of DePIN
        
        allocation_result = self.allocate_capital(simulated_earnings)
        projection = self.get_revenue_projection()
        
        # Generate strategic recommendation
        next_target = None
        for stage in self.stages:
            if not stage.unlocked:
                next_target = stage
                break
        
        recommendation = f"Continue current operations. Next unlock: {next_target.name} (${next_target.min_capital} required)" if next_target else "All stages unlocked. Maximum revenue achieved."
        
        sentinel_data = {
            "agent": "capital_allocation",
            "message": f"Capital: ${self.current_capital:.2f} | Unlocked Stages: {len([s for s in self.stages if s.unlocked])}",
            "status": "GREEN",
            "allocation_result": allocation_result,
            "revenue_projection": projection,
            "recommendation": recommendation,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(self.sentinel_dir / "capital_allocation.done", 'w', encoding='utf-8') as f:
            json.dump(sentinel_data, f, indent=2)
        
        print(f"[CAPITAL] 📊 Projection: ${projection['daily_range'][0]}-${projection['daily_range'][1]}/day")
        print(f"[CAPITAL] 🎯 {recommendation}")

if __name__ == "__main__":
    CapitalAllocationAgent().run()
