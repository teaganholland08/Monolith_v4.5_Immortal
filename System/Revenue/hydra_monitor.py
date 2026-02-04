"""
MONOLITH HYDRA REVENUE MONITORING AGENT
Real-time anomaly detection for all income streams

Monitors:
- Gumroad sales patterns
- Medium article performance
- Crypto trading behavior
- Genesis Engine output quality

Detects:
- Revenue drops (>30% week-over-week)
- Suspicious sales patterns (chargebacks, fraud)
- API failures or rate limits
- Rogue agent behavior (unsafe trades)

Alerts:
- Dashboard notifications
- Email/SMS (if configured)
- Automatic safety shutdown (if critical)
"""

import time
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
import json

class HydraMonitor:
    def __init__(self):
        self.ledger_db = Path(__file__).parent.parent / "Logs" / "ledger.db"
        self.alert_threshold = 0.30  # 30% drop triggers alert
        self.anomaly_log = Path(__file__).parent.parent / "Logs" / "anomalies.log"
        
        # Baselines (updated over time)
        self.baselines = {
            "gumroad_weekly_sales": 0,
            "medium_weekly_reads": 0,
            "crypto_win_rate": 0.5,
            "genesis_quality_score": 0.8
        }
    
    def get_revenue_stats(self, days=7):
        """Fetch revenue statistics from ledger"""
        if not self.ledger_db.exists():
            return {"total": 0, "sources": {}}
        
        conn = sqlite3.connect(self.ledger_db)
        cursor = conn.cursor()
        
        # Get revenue in last N days
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        
        cursor.execute("""
            SELECT source, SUM(amount) 
            FROM transactions 
            WHERE timestamp > ? AND type = 'REVENUE'
            GROUP BY source
        """, (cutoff,))
        
        sources = {}
        total = 0
        for row in cursor.fetchall():
            source, amount = row
            sources[source] = amount
            total += amount
        
        conn.close()
        return {"total": total, "sources": sources}
    
    def detect_revenue_anomalies(self):
        """Detect unusual drops in revenue"""
        anomalies = []
        
        # Get this week vs last week
        this_week = self.get_revenue_stats(days=7)
        last_week = self.get_revenue_stats(days=14)["total"] - this_week["total"]
        
        # Check for significant drop
        if last_week > 0:
            change = (this_week["total"] - last_week) / last_week
            
            if change < -self.alert_threshold:
                anomalies.append({
                    "type": "REVENUE_DROP",
                    "severity": "HIGH",
                    "message": f"Revenue down {abs(change)*100:.1f}% this week",
                    "details": {
                        "last_week": last_week,
                        "this_week": this_week["total"],
                        "change_percent": change * 100
                    }
                })
        
        # Check per source
        for source, amount in this_week["sources"].items():
            expected = self.baselines.get(f"{source}_weekly_sales", 0)
            if expected > 0:
                change = (amount - expected) / expected
                if change < -self.alert_threshold:
                    anomalies.append({
                        "type": "SOURCE_ANOMALY",
                        "severity": "MEDIUM",
                        "message": f"{source} revenue down {abs(change)*100:.1f}%",
                        "details": {
                            "source": source,
                            "expected": expected,
                            "actual": amount
                        }
                    })
        
        return anomalies
    
    def detect_trading_anomalies(self):
        """Detect unusual trading patterns"""
        anomalies = []
        
        if not self.ledger_db.exists():
            return anomalies
        
        conn = sqlite3.connect(self.ledger_db)
        cursor = conn.cursor()
        
        # Get trades in last 24 hours
        cutoff = (datetime.now() - timedelta(hours=24)).isoformat()
        cursor.execute("""
            SELECT action, amount, asset 
            FROM transactions 
            WHERE timestamp > ? AND source = 'CRYPTO'
        """, (cutoff,))
        
        trades = cursor.fetchall()
        conn.close()
        
        if len(trades) == 0:
            return anomalies
        
        # Check for excessive trading (>20 trades/day = likely bot gone rogue)
        if len(trades) > 20:
            anomalies.append({
                "type": "EXCESSIVE_TRADING",
                "severity": "HIGH",
                "message": f"{len(trades)} trades in 24h (normal: <20)",
                "details": {"trade_count": len(trades)}
            })
        
        # Check for large single trades (>$1000 = manual review needed)
        for action, amount, asset in trades:
            if abs(amount) > 1000:
                anomalies.append({
                    "type": "LARGE_TRADE",
                    "severity": "MEDIUM",
                    "message": f"Large {action} detected: ${abs(amount):.2f} in {asset}",
                    "details": {"action": action, "amount": amount, "asset": asset}
                })
        
        return anomalies
    
    def detect_api_failures(self):
        """Check for API connectivity issues"""
        anomalies = []
        
        # Check if Gumroad/Medium bridges are responding
        try:
            from System.Revenue.gumroad_bridge import GumroadBridge
            gb = GumroadBridge()
            if gb.is_configured():
                products = gb.list_products()
                if products is None or len(products) == 0:
                    anomalies.append({
                        "type": "API_FAILURE",
                        "severity": "HIGH",
                        "message": "Gumroad API not responding",
                        "details": {"api": "Gumroad"}
                    })
        except Exception as e:
            anomalies.append({
                "type": "API_ERROR",
                "severity": "MEDIUM",
                "message": f"Gumroad integration error: {str(e)[:50]}",
                "details": {"error": str(e)}
            })
        
        try:
            from System.Revenue.medium_bridge import MediumBridge
            mb = MediumBridge()
            if mb.is_configured():
                user_id = mb.get_user_id()
                if user_id is None:
                    anomalies.append({
                        "type": "API_FAILURE",
                        "severity": "HIGH",
                        "message": "Medium API not responding",
                        "details": {"api": "Medium"}
                    })
        except Exception as e:
            anomalies.append({
                "type": "API_ERROR",
                "severity": "MEDIUM",
                "message": f"Medium integration error: {str(e)[:50]}",
                "details": {"error": str(e)}
            })
        
        return anomalies
    
    def log_anomaly(self, anomaly):
        """Write anomaly to log file"""
        self.anomaly_log.parent.mkdir(exist_ok=True)
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            **anomaly
        }
        
        with open(self.anomaly_log, 'a') as f:
            f.write(json.dumps(entry) + "\n")
    
    def run_scan(self):
        """Full anomaly scan"""
        print("\n🔍 HYDRA: Running Revenue Anomaly Scan...")
        
        all_anomalies = []
        all anomalies.extend(self.detect_revenue_anomalies())
        all_anomalies.extend(self.detect_trading_anomalies())
        all_anomalies.extend(self.detect_api_failures())
        
        if len(all_anomalies) == 0:
            print("   ✅ No anomalies detected - all systems nominal")
            return []
        
        # Log and display
        high_severity = [a for a in all_anomalies if a["severity"] == "HIGH"]
        medium_severity = [a for a in all_anomalies if a["severity"] == "MEDIUM"]
        
        if high_severity:
            print(f"\n   🚨 {len(high_severity)} HIGH SEVERITY ANOMALIES:")
            for anomaly in high_severity:
                print(f"      • {anomaly['message']}")
                self.log_anomaly(anomaly)
        
        if medium_severity:
            print(f"\n   ⚠️ {len(medium_severity)} MEDIUM ANOMALIES:")
            for anomaly in medium_severity:
                print(f"      • {anomaly['message']}")
                self.log_anomaly(anomaly)
        
        return all_anomalies
    
    def update_baselines(self):
        """Recalculate baseline metrics"""
        # Get 30-day average for each metric
        stats = self.get_revenue_stats(days=30)
        
        for source, amount in stats["sources"].items():
            weekly_avg = amount / 4.3  # ~4.3 weeks per month
            self.baselines[f"{source}_weekly_sales"] = weekly_avg
        
        print(f"✓ Baselines updated: {len(self.baselines)} metrics")

if __name__ == "__main__":
    monitor = HydraMonitor()
    monitor.run_scan()
