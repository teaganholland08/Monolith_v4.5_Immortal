import unittest
from datetime import datetime
import sys
import os

# Add parent directory to path so we can import System.Safety
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from System.Safety.hard_deck import HardDeck

class TestHardDeck(unittest.TestCase):
    def setUp(self):
        self.deck = HardDeck()
        # Reset deck for testing
        self.deck.current_daily_spend = 0.0
        self.deck.MAX_DAILY_SPEND = 500.00
        self.deck.trade_timestamps = []

    def test_budget_cap(self):
        """Test that spending > $500 is blocked."""
        # Spend $200 (OK)
        self.assertTrue(self.deck.check_budget(200))
        # Spend $200 (OK)
        self.assertTrue(self.deck.check_budget(200))
        # Spend $200 (FAIL - Total $600)
        self.assertFalse(self.deck.check_budget(200))

    def test_domain_whitelist(self):
        """Test that bad domains are blocked."""
        self.assertTrue(self.deck.check_domain("https://coinbase.com/trade"))
        self.assertTrue(self.deck.check_domain("https://pro.coinbase.com"))
        self.assertFalse(self.deck.check_domain("https://sketchy-crypto-scam.com"))
        self.assertFalse(self.deck.check_domain("http://phishing-site.ru"))

    def test_house_money_scaling(self):
        """Test that profit increases the budget."""
        initial_budget = self.deck.MAX_DAILY_SPEND
        profit = 1000.00
        
        # Register $1000 profit (Should add $500 to budget)
        self.deck.register_profit(profit)
        
        self.assertEqual(self.deck.MAX_DAILY_SPEND, initial_budget + 500.00)
        
        # Now verify we can spend the extra money
        self.deck.current_daily_spend = 500.00 # Maxed out baseline
        self.assertTrue(self.deck.check_budget(400)) # Should allow since limit is now $1000

if __name__ == '__main__':
    unittest.main()
