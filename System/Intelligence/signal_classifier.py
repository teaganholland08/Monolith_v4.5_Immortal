"""
MONOLITH INTELLIGENCE LAYER - Signal Classifier
Turns raw news/data into actionable opportunities

Categories:
- OPPORTUNITY: Make money
- THREAT: Protect assets
- TREND: Ride the wave
- NOISE: Ignore
"""

class SignalClassifier:
    def __init__(self):
        self.money_keywords = [
            "tax break", "exemption", "loophole", "deduction", "credit",
            "subsidy", "grant", "rebate", "incentive"
        ]
        self.threat_keywords = [
            "ban", "restrict", "illegal", "crackdown", "enforcement",
            "audit", "penalty", "fine", "investigation"
        ]
        self.trend_keywords = [
            "boom", "surge", "adoption", "growth", "expansion",
            "demand", "popular", "viral"
        ]
        
    def classify(self, signal):
        """Determine signal type and action"""
        content = signal.get("content", "").lower()
        
        # Check for money opportunities
        if any(kw in content for kw in self.money_keywords):
            return {
                "type": "OPPORTUNITY",
                "action": "CREATE_CONTENT",
                "priority": "HIGH",
                "reasoning": "Tax/financial opportunity detected"
            }
        
        # Check for threats
        if any(kw in content for kw in self.threat_keywords):
            return {
                "type": "THREAT",
                "action": "ALERT_USER",
                "priority": "URGENT",
                "reasoning": "Regulatory threat to current operations"
            }
        
        # Check for trends
        if any(kw in content for kw in self.trend_keywords):
            return {
                "type": "TREND",
                "action": "MONITOR",
                "priority": "MEDIUM",
                "reasoning": "Emerging trend - potential future opportunity"
            }
        
        # Default: noise
        return {
            "type": "NOISE",
            "action": "IGNORE",
            "priority": "LOW",
            "reasoning": "No actionable intelligence"
        }
    
    def generate_action_plan(self, classified_signal, original_signal):
        """Create executable action from signal"""
        signal_type = classified_signal["type"]
        content = original_signal.get("content", "")
        
        if signal_type == "OPPORTUNITY":
            return {
                "step_1": f"Research topic: {content[:100]}",
                "step_2": "Generate article/guide via Genesis Engine",
                "step_3": "Publish to Gumroad/Medium",
                "step_4": "Monitor sales/views",
                "expected_revenue": "$50-500"
            }
        
        elif signal_type == "THREAT":
            return {
                "step_1": "Review current operations for exposure",
                "step_2": "Implement mitigation strategy",
                "step_3": "Consult legal if necessary",
                "step_4": "Update risk profile",
                "expected_loss_prevented": "Unknown - HIGH"
            }
        
        elif signal_type == "TREND":
            return {
                "step_1": "Add to watchlist",
                "step_2": "Set up Google Alert",
                "step_3": "Revisit in 30 days",
                "step_4": "Capitalize if trend accelerates",
                "expected_revenue": "$0-1000 (future)"
            }
        
        return {"note": "No action required"}

if __name__ == "__main__":
    classifier = SignalClassifier()
    
    # Test signals
    test_signals = [
        {"content": "New crypto tax loophole discovered in Wyoming"},
        {"content": "IRS announces crackdown on offshore accounts"},
        {"content": "AI adoption surges 300% in enterprise sector"},
        {"content": "Weather forecast: rain tomorrow"}
    ]
    
    print("🎯 SIGNAL CLASSIFICATION TEST:\n")
    for sig in test_signals:
        result = classifier.classify(sig)
        print(f"Signal: {sig['content']}")
        print(f"  → Type: {result['type']}")
        print(f"  → Action: {result['action']}")
        print(f"  → Priority: {result['priority']}")
        print()
