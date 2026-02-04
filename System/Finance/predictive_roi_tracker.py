"""
PREDICTIVE ROI TRACKER
Calculates exact timeline to next hardware milestone

Features:
- Revenue velocity tracking ($/day average)
- Milestone countdown (days until unlock)
- Auto-approve queue (one-click purchases)
- ROI projections for each tier
"""

import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
import json

class PredictiveROI:
    def __init__(self):
        self.ledger_db = Path(__file__).parent.parent / "Logs" / "ledger.db"
        self.config_file = Path(__file__).parent.parent / "Config" / "treasurer_god_rules.json"
    
    def get_revenue_velocity(self, days=30):
        """
        Calculate average revenue per day over last N days
        
        Returns: (avg_per_day, total_revenue, trend)
        """
        if not self.ledger_db.exists():
            return 0, 0, "FLAT"
        
        conn = sqlite3.connect(self.ledger_db)
        cursor = conn.cursor()
        
        # Last N days
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        
        cursor.execute("""
            SELECT 
                COALESCE(SUM(amount), 0),
                COUNT(*)
            FROM transactions 
            WHERE type = 'REVENUE' AND timestamp > ?
        """, (cutoff,))
        
        total, count = cursor.fetchone()
        
        # Total all-time revenue
        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM transactions
            WHERE type = 'REVENUE'
        """)
        
        all_time = cursor.fetchone()[0]
        
        conn.close()
        
        avg_per_day = total / days if days > 0 else 0
        
        # Determine trend
        if count == 0:
            trend = "FLAT"
        elif avg_per_day > 50:
            trend = "ACCELERATING"
        elif avg_per_day > 10:
            trend = "GROWING"
        else:
            trend = "STARTING"
        
        return avg_per_day, all_time, trend
    
    def predict_milestone(self, target_revenue):
        """
        Predict when revenue will hit target
        
        Returns: (days_until, date_estimated, confidence)
        """
        avg_per_day, current_revenue, trend = self.get_revenue_velocity()
        
        remaining = target_revenue - current_revenue
        
        if remaining <= 0:
            return 0, datetime.now(), "UNLOCKED"
        
        if avg_per_day <= 0:
            return 999, None, "INSUFFICIENT_DATA"
        
        days_until = remaining / avg_per_day
        date_estimated = datetime.now() + timedelta(days=days_until)
        
        # Confidence based on trend
        if trend == "ACCELERATING":
            confidence = "HIGH"
        elif trend == "GROWING":
            confidence = "MEDIUM"
        else:
            confidence = "LOW"
        
        return int(days_until), date_estimated, confidence
    
    def get_next_milestone(self):
        """Get next unlockable tier"""
        from System.Finance.capital_reinvestment import CapitalReinvestment
        
        capital = CapitalReinvestment()
        total_revenue = capital.get_total_revenue()
        next_ms = capital.get_next_milestone(total_revenue)
        
        if next_ms["tier"] == "MAX":
            return None
        
        # Predict timeline
        days, date, confidence = self.predict_milestone(next_ms["threshold"])
        
        return {
            "tier": next_ms["tier"],
            "threshold": next_ms["threshold"],
            "current": total_revenue,
            "remaining": next_ms["remaining"],
            "percent": next_ms["percent"],
            "days_until": days,
            "estimated_date": date.strftime("%Y-%m-%d") if date else "Unknown",
            "confidence": confidence
        }
    
    def generate_briefing(self):
        """Generate predictive ROI briefing"""
        
        avg_per_day, total, trend = self.get_revenue_velocity()
        next_ms = self.get_next_milestone()
        
        print("\n" + "="*60)
        print("📈 PREDICTIVE ROI TRACKER")
        print("="*60)
        
        print(f"\n💰 REVENUE STATUS:")
        print(f"   Total: ${total:,.2f}")
        print(f"   Velocity: ${avg_per_day:.2f}/day (30-day avg)")
        print(f"   Trend: {trend}")
        
        if next_ms:
            print(f"\n🎯 NEXT MILESTONE: {next_ms['tier']}")
            print(f"   Target: ${next_ms['threshold']:,}")
            print(f"   Current: ${next_ms['current']:,.2f} ({next_ms['percent']:.1f}%)")
            print(f"   Remaining: ${next_ms['remaining']:,.2f}")
            
            if next_ms['days_until'] < 999:
                print(f"\n⏱️ PREDICTION:")
                print(f"   Days Until: {next_ms['days_until']} days")
                print(f"   Est. Date: {next_ms['estimated_date']}")
                print(f"   Confidence: {next_ms['confidence']}")
                
                if next_ms['days_until'] <= 7:
                    print(f"\n   🚀 UNLOCK IMMINENT!")
            else:
                print(f"\n   ⚠️ Insufficient data for prediction")
        else:
            print(f"\n🏆 ALL MILESTONES UNLOCKED!")
        
        print("\n" + "="*60 + "\n")
        
        return {
            "velocity": avg_per_day,
            "total": total,
            "trend": trend,
            "next_milestone": next_ms
        }

if __name__ == "__main__":
    tracker = PredictiveROI()
    tracker.generate_briefing()
