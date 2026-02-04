"""
PURCHASING AGENT - Automated Hardware Procurement
Triggers when revenue phases unlock.
"""
import json
from pathlib import Path
from datetime import datetime

class PurchasingAgent:
    def __init__(self):
        self.sentinel_dir = Path(__file__).parent.parent / "Sentinels"
        self.sentinel_dir.mkdir(exist_ok=True)
        self.revenue_sentinel = self.sentinel_dir / "revenue_tracker.done"
        
    def run(self):
        print("[PURCHASER] Checking for unlocked hardware phases...")
        
        if not self.revenue_sentinel.exists():
            print("[PURCHASER] No revenue data found. Waiting.")
            return
        
        with open(self.revenue_sentinel, 'r') as f:
            data = json.load(f)
        
        phases = data.get("phases", [])
        purchased = []
        
        for p in phases:
            if p["status"] == "UNLOCKED":
                print(f"[PURCHASER] TRIGGER: Buying {p['name']}...")
                purchased.append(p["name"])
        
        sentinel_data = {
            "agent": "purchaser",
            "message": f"Procurement scan complete. {len(purchased)} items triggered." if purchased else "Standing by for revenue unlock.",
            "purchased": purchased,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(self.sentinel_dir / "purchaser.done", 'w', encoding='utf-8') as f:
            json.dump(sentinel_data, f, indent=2)
            
        print(f"[PURCHASER] Complete. {len(purchased)} purchases triggered.")

if __name__ == "__main__":
    PurchasingAgent().run()
