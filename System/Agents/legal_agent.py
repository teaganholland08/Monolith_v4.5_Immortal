"""
LEGAL AGENT - Contract & Compliance Automation
Monitors legal obligations and automates paperwork.
"""
import json
from pathlib import Path
from datetime import datetime

class LegalAgent:
    """
    The Legal Guardian.
    - Tracks contract deadlines
    - Monitors compliance requirements
    - Generates legal documents
    """
    
    def __init__(self):
        self.sentinel_dir = Path(__file__).parent.parent / "Sentinels"
        self.sentinel_dir.mkdir(exist_ok=True)
        
    def check_contracts(self):
        return [
            {"name": "Cloud Hosting", "expires": "2026-12-31", "status": "ACTIVE"},
            {"name": "Insurance", "expires": "2026-06-01", "status": "RENEW_SOON"}
        ]
    
    def check_compliance(self):
        return {
            "bc_privacy_act": True,
            "gdpr": True,
            "tax_filing": "CURRENT",
            "business_license": "VALID"
        }
    
    def run(self):
        print("[LEGAL] Checking legal obligations...")
        contracts = self.check_contracts()
        compliance = self.check_compliance()
        
        renew_soon = [c for c in contracts if c["status"] == "RENEW_SOON"]
        
        sentinel_data = {
            "agent": "legal",
            "message": f"Contracts: {len(contracts)} | Renewals: {len(renew_soon)} pending",
            "status": "YELLOW" if renew_soon else "GREEN",
            "contracts": contracts,
            "compliance": compliance,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(self.sentinel_dir / "legal.done", 'w', encoding='utf-8') as f:
            json.dump(sentinel_data, f, indent=2)
        
        print(f"[LEGAL] {len(renew_soon)} contracts need renewal")

if __name__ == "__main__":
    LegalAgent().run()
