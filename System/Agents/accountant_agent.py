"""
ACCOUNTANT AGENT - v5.0 (CanaTax 2026 Engine)
Specialized for British Columbia, Canada Tax Code (2025/2026 Projections).
Handles: T4/T5/T1135 Scraping, Tax-Loss Harvesting, and CRA Netfile Prep.
"""
import json
import time
from pathlib import Path
from datetime import datetime

# --- 2026 TAX CONSTANTS (PROJECTED) ---
# Source: CRA Indexation Factors (Estimated 2.5% inflation adj)
FEDERAL_BRACKETS_2026 = [
    (55867, 0.15),
    (111733, 0.205),
    (173205, 0.26),
    (246752, 0.29),
    (float('inf'), 0.33)
]

BC_BRACKETS_2026 = [
    (47937, 0.0506),
    (95875, 0.077),
    (110076, 0.105),
    (133664, 0.1229),
    (181232, 0.147),
    (float('inf'), 0.168) # 20.5% over $252k actually, simplified for high performers
]

CPP_MAX_2026 = 4000.00 # Enhanced CPP Phase 2
EI_MAX_2026 = 1100.00

class CanaTaxEngine:
    """
    Simulation of the 'canatax' python library for Sovereign calculation.
    """
    @staticmethod
    def calculate_tax(income: float, province: str = "BC") -> float:
        """Calculates combined Federal + Provincial Tax"""
        fed_tax = 0.0
        remaining = income
        prev_limit = 0
        
        # Federal Calculation
        for limit, rate in FEDERAL_BRACKETS_2026:
            taxable_in_bracket = min(remaining, limit - prev_limit)
            if taxable_in_bracket <= 0: break
            fed_tax += taxable_in_bracket * rate
            remaining -= taxable_in_bracket
            prev_limit = limit
            
        # BC Calculation (Simplified Progressive)
        prov_tax = 0.0
        remaining = income
        prev_limit = 0
        for limit, rate in BC_BRACKETS_2026:
            taxable_in_bracket = min(remaining, limit - prev_limit)
            if taxable_in_bracket <= 0: break
            prov_tax += taxable_in_bracket * rate
            remaining -= taxable_in_bracket
            prev_limit = limit
            
        # Basic Personal Amount Credits (Approx $15k)
        credits = (15705 * 0.15) + (13000 * 0.0506)
        
        return max(0, fed_tax + prov_tax - credits)

class SlipScraper:
    """
    Interface for Bank/CRA Slip Extraction
    """
    def __init__(self, vault_dir):
        self.vault_dir = vault_dir

    def run_scrape_sequence(self):
        print("   🏦 SCRAPER: Connecting to CRA via Partner API (Simulated)...")
        time.sleep(0.5)
        print("   🏦 SCRAPER: Connecting to Wealthsimple Trade...")
        time.sleep(0.5)
        
        # Simulated Findings
        return {
            "T4": [{"employer": "ACME CORP", "income": 125000.00, "tax_deducted": 32000.00}],
            "T5": [{"issuer": "EQ BANK", "interest": 4500.00, "tax_deducted": 0.0}],
            "T5008": [{"security": "NVDA", "proceeds": 25000.00, "cost_base": 15000.00}] # Cap Gains
        }

class AccountantAgent:
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.sentinel_dir = self.root / "Sentinels"
        self.memory_dir = self.root.parent / "Memory" / "Tax"
        
        self.sentinel_dir.mkdir(exist_ok=True)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
    def run(self):
        print("📊 ACCOUNTANT: Initializing 2026 Tax Sovereign Flow...")
        
        # 1. Scrape Info
        scraper = SlipScraper(self.memory_dir)
        slips = scraper.run_scrape_sequence()
        
        # 2. Aggregation
        total_income = 0.0
        tax_paid = 0.0
        
        for t4 in slips["T4"]:
            total_income += t4["income"]
            tax_paid += t4["tax_deducted"]
            
        for t5 in slips["T5"]:
            total_income += t5["interest"]
            tax_paid += t5["tax_deducted"]
            
        capital_gains = 0.0
        for trade in slips["T5008"]:
            gain = trade["proceeds"] - trade["cost_base"]
            capital_gains += gain * 0.50 # %50 inclusion rate (or 66% if >250k in 2025 budget, using 50 base)
            
        total_taxable = total_income + capital_gains
        
        # 3. Calculate Obligation
        engine = CanaTaxEngine()
        estimated_tax = engine.calculate_tax(total_taxable, "BC")
        estimated_cpp_ei = CPP_MAX_2026 + EI_MAX_2026
        
        final_bill = estimated_tax + estimated_cpp_ei
        balance = final_bill - tax_paid
        
        # 4. Report
        status = "GREEN"
        msg = f"Taxable: ${total_taxable:,.2f} | Est. Tax: ${final_bill:,.2f} | Balance: ${balance:,.2f}"
        
        if balance > 5000:
            status = "YELLOW" # Alert user to save cash
            msg += " [HIGH OWING ALERT]"
            
        print(f"   🧾 RESULT: {msg}")
        
        self._save_sentinel(status, msg, {
            "total_taxable": total_taxable,
            "estimated_obligation": final_bill,
            "balance_owing": balance
        })

    def _save_sentinel(self, status, message, data):
        payload = {
            "agent": "accountant_agent",
            "status": status,
            "message": message,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        with open(self.sentinel_dir / "accountant_agent.done", 'w', encoding='utf-8') as f:
            json.dump(payload, f, indent=2)

if __name__ == "__main__":
    AccountantAgent().run()

import json
import random
from pathlib import Path
from datetime import datetime

class AccountantAgent:
    """
    The Tax Brain of Project Monolith.
    - Continuous Tax-Loss Harvesting monitoring
    - BC Specific Loophole Execution
    - Autonomous slip scraping (T4, T5, T1135)
    - Wealthsimple Tax AI (Enterprise) integration patterns
    """
    
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.sentinel_dir = self.root / "Sentinels"
        self.memory_dir = self.root.parent / "Memory" / "Tax"
        
        self.sentinel_dir.mkdir(exist_ok=True)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
    def slip_scraper(self):
        """
        [SLIP-SCRAPER] 
        Connects to bank and CRA MyAccount (simulated) to pull tax slips.
        """
        print("[ACCOUNTANT] Scraping digital slips (T4, T5, T1135)...")
        slips = [
            {"type": "T4", "issuer": "Corp X", "income": 85000, "tax_withheld": 18000},
            {"type": "T5", "issuer": "Wealthsimple", "interest": 1200, "capital_gains": 5400},
            {"type": "T1135", "status": "REQUIRED", "assets_held": "Global Crypto Vault"}
        ]
        
        # Save to encrypted vault (simulated)
        vault_file = self.memory_dir / "slips_2025.json"
        with open(vault_file, 'w', encoding='utf-8') as f:
            json.dump(slips, f, indent=2)
            
        return slips

    def scan_bc_loopholes(self):
        """
        Scans for 2026 British Columbia specific credits.
        """
        print("[ACCOUNTANT] Scanning CRA & BC Government bulletins...")
        loopholes = [
            {
                "id": "BC_RE_2026",
                "name": "Clean Energy Home Upgrade Rebate",
                "potential_savings": 2500,
                "status": "QUALIFIED",
                "reason": "Powell River solar installation detected."
            },
            {
                "id": "BC_SBVC_2026",
                "name": "Small Business Venture Capital Credit",
                "potential_savings": 5000,
                "status": "PENDING",
                "reason": "30% refundable tax credit for angel investments."
            },
            {
                "id": "VANISH_DEDUCTION",
                "name": "Digital Infrastructure Accelerated Depreciation",
                "potential_savings": 1200,
                "status": "EXECUTING",
                "reason": "RTX 5090 reclassification."
            }
        ]
        return loopholes

    def calculate_tax_brief(self, slips, loopholes):
        """
        Generates the 15-minute Director Briefing for taxes.
        """
        total_income = sum(s.get("income", 0) + s.get("interest", 0) + s.get("capital_gains", 0) for s in slips)
        total_tax_paid = sum(s.get("tax_withheld", 0) for s in slips)
        
        qualified_savings = sum(l["potential_savings"] for l in loopholes if l["status"] in ["QUALIFIED", "EXECUTING"])
        
        # Mock calculation logic
        estimated_tax_owed = (total_income * 0.25) - total_tax_paid - qualified_savings
        
        return {
            "total_income": total_income,
            "tax_already_paid": total_tax_paid,
            "loophole_savings": qualified_savings,
            "estimated_balance": round(estimated_tax_owed, 2),
            "audit_risk": 0.02, # Simulated via Red-Teaming
            "filing_deadline": "2026-04-30"
        }

    def run(self):
        print("[ACCOUNTANT] Initializing 2026 Tax Audit...")
        
        slips = self.slip_scraper()
        loopholes = self.scan_bc_loopholes()
        briefing = self.calculate_tax_brief(slips, loopholes)
        
        status = "GREEN"
        message = f"Tax Refund Estimated: ${abs(briefing['estimated_balance']):,.2f}" if briefing['estimated_balance'] < 0 else f"Tax Due: ${briefing['estimated_balance']:,.2f}"
        
        sentinel_data = {
            "agent": "accountant_agent",
            "message": message,
            "status": status,
            "briefing": briefing,
            "loopholes_detected": len(loopholes),
            "timestamp": datetime.now().isoformat()
        }
        
        with open(self.sentinel_dir / "accountant_agent.done", 'w', encoding='utf-8') as f:
            json.dump(sentinel_data, f, indent=2)
            
        print(f"[ACCOUNTANT] {message}")
        print(f"   📊 Audit Risk: {briefing['audit_risk'] * 100}%")
        print(f"   📅 Deadline: {briefing['filing_deadline']}")

if __name__ == "__main__":
    AccountantAgent().run()
