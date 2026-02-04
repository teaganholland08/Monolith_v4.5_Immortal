"""
MONOLITH LEGAL ARBITRAGE LAYER - Tax Optimizer
Jurisdictional Analysis & Global Tax Minimization

Finds optimal tax jurisdiction based on:
- Income sources
- Citizenship
- Mobility
- Risk tolerance
"""

class TaxOptimizer:
    def __init__(self):
        self.jurisdictions = self._load_jurisdiction_database()
        
    def _load_jurisdiction_database(self):
        """195+ countries with tax profiles"""
        return {
            "UAE": {
                "country": "United Arab Emirates",
                "income_tax": 0,
                "capital_gains": 0,
                "corporate_tax": 9,  # New as of 2023
                "vat": 5,
                "residency_requirement": "UAE Golden Visa (or 183 days)",
                "citizenship_available": False,
                "banking_privacy": "High",
                "cost_of_living_index": 75,  # 100 = NYC
                "pro": ["0% income tax", "Stable government", "Modern infrastructure"],
                "con": ["Hot climate", "9% corporate tax (new)", "Expensive housing"]
            },
            "PORTUGAL": {
                "country": "Portugal",
                "income_tax": 28,  # Progressive up to 48%
                "capital_gains": 28,
                "capital_gains_crypto": 0,  # Exemption for crypto held >1 year
                "corporate_tax": 21,
                "vat": 23,
                "residency_requirement": "D7 Visa (passive income) or Digital Nomad Visa",
                "citizenship_available": True,  # After 5 years
                "banking_privacy": "Medium",
                "cost_of_living_index": 50,
                "pro": ["0% crypto gains", "EU citizenship path", "Low cost of living"],
                "con": ["High VAT", "Bureaucracy", "Language barrier"]
            },
            "PUERTO_RICO": {
                "country": "Puerto Rico (US Territory)",
                "income_tax": 4,  # Act 60
                "capital_gains": 0,  # Act 60
                "corporate_tax": 4,
                "vat": 11.5,  # IVU
                "residency_requirement": "183 days/year physical presence",
                "citizenship_available": "Already US citizens",
                "banking_privacy": "Low (US jurisdiction)",
                "cost_of_living_index": 60,
                "pro": ["Keep US passport", "4% tax", "No exit tax"],
                "con": ["Hurricane risk", "Must actually live there", "Infrastructure issues"]
            },
            "SINGAPORE": {
                "country": "Singapore",
                "income_tax": 22,  # Progressive up to 24%
                "capital_gains": 0,
                "corporate_tax": 17,
                "vat": 9,  # GST
                "residency_requirement": "Employment Pass or EntrePass",
                "citizenship_available": "Very difficult",
                "banking_privacy": "Very High",
                "cost_of_living_index": 100,
                "pro": ["0% capital gains", "Stable banking", "Safe country"],
                "con": ["Expensive", "Strict laws", "Hard to get residency"]
            },
            "PANAMA": {
                "country": "Panama",
                "income_tax": 25,  # Territorial (only local income)
                "capital_gains": 10,
                "corporate_tax": 25,
                "vat": 7,  # ITBMS
                "residency_requirement": "Friendly Nations Visa (easy)",
                "citizenship_available": True,  # After 5 years
                "banking_privacy": "High",
                "cost_of_living_index": 45,
                "pro": ["Territorial taxation", "Easy residency", "USD economy"],
                "con": ["Political instability", "Corruption", "Infrastructure"]
            },
            "SWITZERLAND": {
                "country": "Switzerland",
                "income_tax": 40,  # Varies by canton
                "capital_gains": 0,  # Personal capital gains tax-free
                "corporate_tax": 14.9,
                "vat": 7.7,
                "residency_requirement": "Lump sum tax (for wealthy) or employment",
                "citizenship_available": True,  # After 10 years (very expensive)
                "banking_privacy": "High",
                "cost_of_living_index": 130,
                "pro": ["0% capital gains", "Strongest privacy", "Political stability"],
                "con": ["Very expensive", "Hard to immigrate", "High income tax"]
            }
        }
    
    def calculate_net_income(self, gross_income, jurisdiction, income_type="employment"):
        """Calculate after-tax income in a specific jurisdiction"""
        jur = self.jurisdictions.get(jurisdiction)
        if not jur:
            return 0
        
        # Simplified calculation
        if income_type == "employment":
            tax_rate = jur["income_tax"] / 100
        elif income_type == "capital_gains":
            if jurisdiction == "PORTUGAL" and "capital_gains_crypto" in jur:
                tax_rate = jur["capital_gains_crypto"] / 100
            else:
                tax_rate = jur["capital_gains"] / 100
        else:
            tax_rate = jur["corporate_tax"] / 100
        
        net = gross_income * (1 - tax_rate)
        return net
    
    def find_optimal_jurisdiction(self, 
                                   income_amount, 
                                   income_type="employment",
                                   us_citizen=True,
                                   willing_to_relocate=True):
        """Returns best jurisdiction for maximum after-tax income"""
        
        results = []
        for jur_id, jur_data in self.jurisdictions.items():
            # Filter by citizenship constraints
            if us_citizen and jur_id not in ["PUERTO_RICO", "UAE", "PORTUGAL", "PANAMA", "SINGAPORE"]:
                continue  # Skip complex jurisdictions for demo
            
            if not willing_to_relocate and jur_id != "PUERTO_RICO":
                continue  # Can't benefit without moving
            
            net = self.calculate_net_income(income_amount, jur_id, income_type)
            
            results.append({
                "jurisdiction": jur_id,
                "country": jur_data["country"],
                "net_income": net,
                "tax_paid": income_amount - net,
                "effective_rate": ((income_amount - net) / income_amount * 100),
                "requirements": jur_data["residency_requirement"],
                "pros": jur_data["pro"],
                "cons": jur_data["con"]
            })
        
        # Sort by net income (highest first)
        results.sort(key=lambda x: x["net_income"], reverse=True)
        return results
    
    def generate_relocation_plan(self, target_jurisdiction):
        """Step-by-step guide to move to optimal jurisdiction"""
        jur = self.jurisdictions.get(target_jurisdiction)
        if not jur:
            return []
        
        plans = {
            "PUERTO_RICO": [
                "1. Apply for Puerto Rico Act 60 Decree ($5k-10k application)",
                "2. Establish bona fide residency (buy/rent property)",
                "3. Spend 183+ days/year in Puerto Rico",
                "4. Open Puerto Rico bank account",
                "5. File final US state tax return (if moving from a state)",
                "6. Begin enjoying 4% tax rate"
            ],
            "UAE": [
                "1. Apply for UAE Golden Visa ($10k+) or company visa",
                "2. Open Emirates NBD bank account",
                "3. Register Free Zone company ($5k-15k)",
                "4. Obtain Emirates ID",
                "5. Rent property (required for visa)",
                "6. File US exit tax return if renouncing (only if >$2M net worth)"
            ],
            "PORTUGAL": [
                "1. Apply for D7 Visa (passive income) or Digital Nomad Visa",
                "2. Open Portuguese bank account",
                "3. Register for NHR (Non-Habitual Resident) tax status",
                "4. Rent property for 1 year minimum",
                "5. Obtain residence card",
                "6. After 5 years, eligible for EU citizenship"
            ]
        }
        
        return plans.get(target_jurisdiction, ["Manual research required"])

if __name__ == "__main__":
    optimizer = TaxOptimizer()
    
    print("🌍 TAX OPTIMIZATION ANALYSIS")
    print("="*60)
    print("\nScenario: $250,000 crypto capital gains")
    print("Current Location: California, USA (37% federal + 13.3% state = 50.3%)")
    print()
    
    results = optimizer.find_optimal_jurisdiction(
        income_amount=250000,
        income_type="capital_gains",
        us_citizen=True,
        willing_to_relocate=True
    )
    
    print("TOP 3 JURISDICTIONS:")
    for i, res in enumerate(results[:3], 1):
        print(f"\n{i}. {res['country']} ({res['jurisdiction']})")
        print(f"   Net Income: ${res['net_income']:,.0f}")
        print(f"   Tax Paid: ${res['tax_paid']:,.0f}")
        print(f"   Effective Rate: {res['effective_rate']:.1f}%")
        print(f"   Requirements: {res['requirements']}")
    
    print("\n\n📋 RELOCATION PLAN (Puerto Rico):")
    plan = optimizer.generate_relocation_plan("PUERTO_RICO")
    for step in plan:
        print(f"   {step}")
