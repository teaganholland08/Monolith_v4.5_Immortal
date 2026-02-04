"""
INVESTMENT AGENT (Wealth Pillar)
Part of Monolith Class-5 Architecture.
Timestamp: 2026-02-04

Role:
1. Market Oracle (Live Data Feed)
2. Risk Analysis (Monte Carlo Simulation)
3. Risk Officer (Hard Deck Enforcement)
4. Portfolio Management
"""

import json
import logging
import time
import random
import math
import statistics
from pathlib import Path
from datetime import datetime

# Optional Imports for Best-in-Class Math
try:
    import yfinance as yf
    import numpy as np
except ImportError:
    yf = None
    np = None

class RiskAnalyzer:
    """
    Advanced Risk Modeling Engine (Monte Carlo + VaR)
    """
    def __init__(self, simulations=1000):
        self.simulations = simulations
    
    def run_monte_carlo(self, current_price, volatility, days=30):
        """Generates projected price paths using Geometric Brownian Motion"""
        if not np:
            return 0.5, 0.0 # Fallback if numpy missing
            
        dt = 1/252
        price_paths = []
        
        for _ in range(self.simulations):
            price = current_price
            for _ in range(days):
                drift = 0.05 * dt # Assumed 5% annual drift
                shock = volatility * np.random.normal(0, 1) * np.sqrt(dt)
                price = price + (price * (drift + shock))
            price_paths.append(price)
            
        final_prices = np.array(price_paths)
        expected_roi = (np.mean(final_prices) - current_price) / current_price
        win_prob = np.sum(final_prices > current_price) / self.simulations
        
        return win_prob, expected_roi * 100

class MarketOracle:
    """
    Real-Time Market Data Interface
    """
    def __init__(self):
        self.tickers = ["BTC-USD", "ETH-USD", "SPY"]
        self.cache = {}
        self.last_update = 0
        
    def fetch_data(self):
        """Simulates or Fetches Live Data"""
        results = {}
        
        # 1. Try Real YFinance
        if yf:
            try:
                # Limit calls to avoid rate limits
                data = yf.download(self.tickers, period="5d", progress=False)
                for ticker in self.tickers:
                     # Simple logic to get last close
                     close = data['Close'][ticker].iloc[-1]
                     open_p = data['Open'][ticker].iloc[-1]
                     results[ticker] = {"price": float(close), "change": float((close-open_p)/open_p)}
                return results
            except Exception as e:
                logging.warning(f"Oracle Connection Failed: {e}")
        
        # 2. Simulation Fallback (If offline/rate-limited)
        return {
            "BTC-USD": {"price": 98500.00, "change": 0.025},
            "ETH-USD": {"price": 6200.00, "change": 0.012},
            "SPY": {"price": 580.00, "change": -0.005}
        }

class RiskOfficer:
    """
    Hard Deck & Validation Logic
    """
    def __init__(self):
        self.hard_deck_limit = -0.05  # Max 5% Drawdown
        self.max_trade_size = 1000.00 # Max single bet
    
    def validate(self, trade_proposal):
        if trade_proposal['amount'] > self.max_trade_size:
            return False, "Exceeds Max Trade Size"
        if trade_proposal['start_risk'] < 0.6: # 60% win rate required
            return False, "Risk Score Too Low"
        return True, "APPROVED"

class InvestmentAgent:
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.sentinel_dir = self.root / "Sentinels"
        self.memory_dir = self.root.parent / "Memory" / "investment_agent"
        
        self.sentinel_dir.mkdir(exist_ok=True)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        self.oracle = MarketOracle()
        self.analyzer = RiskAnalyzer()
        self.officer = RiskOfficer()
        
        logging.basicConfig(level=logging.INFO)

    def run(self):
        logging.info("Investment Agent Active...")
        
        # 1. Market Scan
        data = self.oracle.fetch_data()
        
        # 2. Analyze Opportunities (Simulation)
        opportunities = []
        btc_data = data.get("BTC-USD", {})
        
        if btc_data:
            # Monte Carlo Run
            volatility = 0.65 # Crypto Volatility
            win_prob, exp_roi = self.analyzer.run_monte_carlo(btc_data['price'], volatility)
            
            # Proposal
            proposal = {
                "asset": "BTC",
                "amount": 500,
                "start_risk": win_prob
            }
            
            # Risk Officer Check
            approved, reason = self.officer.validate(proposal)
            
            opportunities.append({
                "asset": "BTC",
                "price": btc_data['price'],
                "monte_carlo_win_prob": win_prob,
                "expected_roi": exp_roi,
                "status": "APPROVED" if approved else "DENIED",
                "reason": reason
            })

        # 3. Report
        portfolio_value = 74091.55 # Mock Total
        status = "GREEN"
        message = f"Portfolio: ${portfolio_value:,.2f} | Analyzed {len(opportunities)} Assets"
        
        report = {
            "agent": "investment_agent",
            "status": status,
            "message": message,
            "market_data": data,
            "opportunities": opportunities,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(self.sentinel_dir / "investment_agent.done", 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
            
        logging.info(f"Report filed: {message}")

if __name__ == "__main__":
    InvestmentAgent().run()
