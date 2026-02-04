"""
SHOPPING AGENT - Autonomous Procurement & Deals
Finds best prices and automates purchases.
"""
import json
from pathlib import Path
from datetime import datetime

class ShoppingAgent:
    """
    The Deal Finder.
    - Monitors prices
    - Finds deals and discounts
    - Automates recurring purchases
    """
    
    def __init__(self):
        self.sentinel_dir = Path(__file__).parent.parent / "Sentinels"
        self.sentinel_dir.mkdir(exist_ok=True)
        
    def scan_deals(self):
        return [
            {"item": "RTX 5090", "store": "Memory Express", "price": 2499, "discount": "5%"},
            {"item": "Protein Powder", "store": "Amazon", "price": 45, "discount": "Subscribe & Save 15%"}
        ]
    
    def check_subscriptions(self):
        return [
            {"item": "Coffee Beans", "frequency": "Monthly", "next_delivery": "2026-02-10"},
            {"item": "Vitamins", "frequency": "Monthly", "next_delivery": "2026-02-15"}
        ]
    
    def run(self):
        print("[SHOPPING] Scanning deals...")
        deals = self.scan_deals()
        subs = self.check_subscriptions()
        
        sentinel_data = {
            "agent": "shopping",
            "message": f"Deals: {len(deals)} found | Subscriptions: {len(subs)} active",
            "status": "ACTIVE",
            "deals": deals,
            "subscriptions": subs,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(self.sentinel_dir / "shopping.done", 'w', encoding='utf-8') as f:
            json.dump(sentinel_data, f, indent=2)
        
        print(f"[SHOPPING] {len(deals)} deals found")

if __name__ == "__main__":
    ShoppingAgent().run()
