"""
REVENUE EXECUTOR - The Hammer of Project Monolith (v5.0)
Purpose: High-speed transaction execution based on approved agent intent.
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# Add root to path
root_path = Path(__file__).parent.parent.parent
sys.path.append(str(root_path))

from System.Core.monetization_bridge import get_bridge

class RevenueExecutor:
    """
    The final step in the wealth pipeline.
    Receives approved intents and executes them via the bridge.
    """
    
    def __init__(self):
        self.bridge = get_bridge()
        self.sentinel_dir = Path(__file__).parent.parent / "Sentinels"
        self.sentinel_dir.mkdir(exist_ok=True)
        
    def process_intent(self, intent: Dict[str, Any]) -> Dict:
        """
        Processes a wealth intent (Arbitrage, Trade, Listing).
        Expected schema:
        {
            "origin": "investment_agent",
            "type": "CEX_TRADE",
            "params": {...},
            "auditor_approved": True
        }
        """
        if not intent.get("auditor_approved", False):
            print("[EXECUTOR] 🛑 REJECTED: Intent lacks Auditor approval.")
            return {"status": "REJECTED", "reason": "NO_AUDITOR_SIG"}
            
        action_type = intent.get("type")
        params = intent.get("params", {})
        
        print(f"[EXECUTOR] ⚡ EXECUTING: {action_type} for {intent.get('origin')}")
        
        result = {"status": "UNKNOWN"}
        
        if action_type == "CEX_TRADE":
            result = self.bridge.execute_cex_trade(
                params.get("exchange"), 
                params.get("symbol"), 
                params.get("side"), 
                params.get("amount")
            )
        elif action_type == "DEFI_SWAP":
            result = self.bridge.execute_defi_swap(
                params.get("chain"),
                params.get("token_in"),
                params.get("token_out"),
                params.get("amount")
            )
        elif action_type == "FIAT_LISTING":
            result = self.bridge.list_ip_asset(
                params.get("platform"),
                params.get("asset_name"),
                params.get("price")
            )
            
        # Log success/failure
        self.bridge.log_transaction(action_type, {"intent": intent, "result": result})
        
        return result

    def run(self):
        """Simulated loop checking for execution signals"""
        # In a real impl, this would sub to a Redis/RabbitMQ queue
        # For now, we file a sentinel indicating the executor is ready
        sentinel_data = {
            "agent": "revenue_executor",
            "status": "ACTIVE",
            "message": "Executor Bridge Online - Awaiting Approved Intents",
            "timestamp": datetime.now().isoformat()
        }
        
        with open(self.sentinel_dir / "revenue_executor.done", 'w', encoding='utf-8') as f:
            json.dump(sentinel_data, f, indent=2)
            
        print("[EXECUTOR] ✅ Ready for deployment. External financial rails integrated.")

if __name__ == "__main__":
    RevenueExecutor().run()
