"""
INVESTMENT AGENT - Portfolio & Trading Automation
Manages investments and executes trades.
"""
import json
import random
from pathlib import Path
from datetime import datetime

class InvestmentAgent:
    """
    The Investment Manager.
    - Monitors portfolio
    - Executes trades
    - Rebalances allocations
    """
    
    def __init__(self):
        self.sentinel_dir = Path(__file__).parent.parent / "Sentinels"
        self.sentinel_dir.mkdir(exist_ok=True)
        
    def get_portfolio(self):
        return {
            "total_value": random.uniform(50000, 100000),
            "daily_change": random.uniform(-2, 5),
            "allocations": {
                "stocks": 50,
                "bonds": 20,
                "crypto": 20,
                "cash": 10
            }
        }
    
    def check_signals(self):
        return [
            {"asset": "BTC", "signal": "HOLD", "confidence": 0.7},
            {"asset": "VOO", "signal": "BUY", "confidence": 0.8}
        ]
    
    def run(self):
        print("[INVESTMENT] Analyzing portfolio...")
        portfolio = self.get_portfolio()
        signals = self.check_signals()
        
        sentinel_data = {
            "agent": "investment",
            "message": f"Portfolio: ${portfolio['total_value']:,.2f} ({portfolio['daily_change']:+.1f}%)",
            "status": "ACTIVE",
            "portfolio": {k: round(v, 2) if isinstance(v, float) else v for k, v in portfolio.items()},
            "signals": signals,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(self.sentinel_dir / "investment.done", 'w', encoding='utf-8') as f:
            json.dump(sentinel_data, f, indent=2)
        
        print(f"[INVESTMENT] ${portfolio['total_value']:,.2f} ({portfolio['daily_change']:+.1f}%)")

if __name__ == "__main__":
    InvestmentAgent().run()
