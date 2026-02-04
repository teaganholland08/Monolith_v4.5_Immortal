"""
THE HARD DECK (Layer 1 Safety)
Deterministic Code. Non-negotiable.
"""
from datetime import datetime, timedelta
from urllib.parse import urlparse

class HardDeck:
    def __init__(self):
        # 1. THE BUDGET CAP (ADAPTIVE)
        self.BASELINE_BUDGET = 500.00
        self.MAX_DAILY_SPEND = self.BASELINE_BUDGET
        self.current_daily_spend = 0.0
        self.daily_profit_buffer = 0.0 # "House Money"
        self.last_reset = datetime.now().date()

        # 2. THE WHITELIST LOCK
        self.ALLOWED_DOMAINS = [
            "coinbase.com", 
            "mercury.com", 
            "amazon.com", 
            "adobe.com",
            "google.com",
            "openai.com",
            "github.com",
            "upwork.com",
            "fiverr.com",
            "stock.adobe.com"
        ]

        # 3. THE RATE LIMITER
        self.MAX_TRADES_PER_HOUR = 5
        self.trade_timestamps = []

    def check_budget(self, amount: float) -> bool:
        """Ensures we don't burn the vault."""
        # Reset daily if next day
        if datetime.now().date() > self.last_reset:
            self.current_daily_spend = 0.0
            self.daily_profit_buffer = 0.0 # Reset House Money
            self.MAX_DAILY_SPEND = self.BASELINE_BUDGET # Reset Cap
            self.last_reset = datetime.now().date()
            print("🔄 HARD DECK: Daily Budget Reset to Baseline ($500).")

        if (self.current_daily_spend + amount) > self.MAX_DAILY_SPEND:
            print(f"🛑 HARD DECK: DENIED. ${amount:.2f} exceeds remaining budget (${self.MAX_DAILY_SPEND - self.current_daily_spend:.2f}).")
            return False
        
        self.current_daily_spend += amount
        return True

    def register_profit(self, profit: float):
        """The 'House Money' Rule: 50% of profit increases today's budget."""
        scaling_factor = 0.50 
        added_budget = profit * scaling_factor
        self.MAX_DAILY_SPEND += added_budget
        self.daily_profit_buffer += added_budget
        print(f"📈 HARD DECK: Budget Scaled! +${added_budget:.2f} (New Limit: ${self.MAX_DAILY_SPEND:.2f})")

    def check_domain(self, url: str) -> bool:
        """Ensures we don't visit malware/gambling sites."""
        try:
            domain = urlparse(url).netloc
            # Handle subdomains roughly
            base_domain = ".".join(domain.split('.')[-2:]) 
            if base_domain in self.ALLOWED_DOMAINS:
                return True
            if domain in self.ALLOWED_DOMAINS:
                return True
            
            print(f"🛑 HARD DECK: DENIED. Domain '{domain}' not in Whitelist.")
            return False
        except:
            return False

    def check_rate_limit(self) -> bool:
        """Ensures no High-Frequency glitches."""
        now = datetime.now()
        # Filter trades older than 1 hour
        self.trade_timestamps = [t for t in self.trade_timestamps if now - t < timedelta(hours=1)]
        
        if len(self.trade_timestamps) >= self.MAX_TRADES_PER_HOUR:
            print(f"🛑 HARD DECK: DENIED. HFT Limit Reached ({self.MAX_TRADES_PER_HOUR}/hr).")
            return False
        
        self.trade_timestamps.append(now)
        return True

    def nuclear_key_check(self, amount: float) -> bool:
        """Layer 4: Human Approval for > $1000"""
        if amount > 1000:
            print(f"☢️ NUCLEAR KEY REQUIRED: Spend ${amount} > $1000.")
            # In production, this waits for hardware button
            # For simulation, we assume user is monitoring
            print("   -> 🛑 SYSTEM PAUSED. WAITING FOR HUMAN APPROVAL...")
            # return input("   -> APPROVE? (y/n): ").lower() == 'y'
            return False # Default to SAFE
        return True
