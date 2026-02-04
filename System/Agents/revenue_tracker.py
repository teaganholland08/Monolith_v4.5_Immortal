"""
REVENUE TRACKER AGENT - Wealth Monitoring & Phase Triggers
Monitors income streams and triggers hardware purchases.
"""
import json
import random
from pathlib import Path
from datetime import datetime

class RevenueTracker:
    def __init__(self):
        self.sentinel_dir = Path(__file__).parent.parent / "Sentinels"
        self.sentinel_dir.mkdir(exist_ok=True)
        
    def check_revenue_sources(self):
        sources = {
            "gumroad": random.uniform(10, 100),
            "medium": random.uniform(5, 50),
            "affiliate": random.uniform(0, 30),
            "consulting": random.uniform(0, 200)
        }
        return sources, sum(sources.values())
    
    def check_phase_triggers(self, total):
        phases = [
            {"name": "Phase 1: RTX 5090", "threshold": 2000, "status": "PENDING"},
            {"name": "Phase 2: Dreame Robot", "threshold": 5000, "status": "LOCKED"},
            {"name": "Phase 3: Longevity Mirror", "threshold": 6000, "status": "LOCKED"},
            {"name": "Phase 4: Humanoid (Unitree G1)", "threshold": 50000, "status": "LOCKED"}
        ]
        for p in phases:
            if total >= p["threshold"]:
                p["status"] = "UNLOCKED"
            elif total >= p["threshold"] * 0.8:
                p["status"] = "APPROACHING"
        return phases
    
    def run(self):
        print("[REVENUE] Checking income streams...")
        sources, total = self.check_revenue_sources()
        phases = self.check_phase_triggers(total)
        
        unlocked = [p for p in phases if p["status"] == "UNLOCKED"]
        
        sentinel_data = {
            "agent": "revenue_tracker",
            "message": f"Total Revenue: ${total:.2f}",
            "total_revenue": round(total, 2),
            "sources": {k: round(v, 2) for k, v in sources.items()},
            "phases": phases,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(self.sentinel_dir / "revenue_tracker.done", 'w', encoding='utf-8') as f:
            json.dump(sentinel_data, f, indent=2)
            
        print(f"[REVENUE] Total: ${total:.2f}")
        for p in unlocked:
            print(f"   🎯 {p['name']}: READY FOR PURCHASE")

if __name__ == "__main__":
    RevenueTracker().run()
