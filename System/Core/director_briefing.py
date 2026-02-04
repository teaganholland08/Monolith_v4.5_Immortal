"""
MONOLITH DAILY DIRECTOR BRIEFING
15-minute review system for autonomous operation

Purpose: User acts as Director, AI acts as Operator
User Time: 15 minutes/day max
AI Time: 23 hours 45 minutes autonomous

Briefing Structure:
- Minutes 1-5: Review overnight activity
- Minutes 6-10: Approve high-stakes decisions
- Minutes 11-15: Set strategic direction

Displays:
- Revenue progress toward milestones
- Purchase recommendations
- Intelligence alerts
- Anomaly warnings
- Strategic opportunities
"""

import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
import json

class DirectorBriefing:
    def __init__(self):
        self.ledger_db = Path(__file__).parent.parent / "Logs" / "ledger.db"
        self.briefing_history = Path(__file__).parent.parent / "Logs" / "briefings"
        self.briefing_history.mkdir(exist_ok=True)
        
    def get_overnight_activity(self):
        """Revenue/trades in last 24 hours"""
        if not self.ledger_db.exists():
            return []
        
        conn = sqlite3.connect(self.ledger_db)
        cursor = conn.cursor()
        
        cutoff = (datetime.now() - timedelta(hours=24)).isoformat()
        
        cursor.execute("""
            SELECT source, action, amount, timestamp 
            FROM transactions 
            WHERE timestamp > ? 
            ORDER BY timestamp DESC
        """, (cutoff,))
        
        activities = []
        for row in cursor.fetchall():
            source, action, amount, timestamp = row
            activities.append({
                "source": source,
                "action": action,
                "amount": amount,
                "timestamp": timestamp
            })
        
        conn.close()
        return activities
    
    def get_pending_decisions(self):
        """High-stakes items awaiting approval"""
        from System.Finance.capital_reinvestment import CapitalReinvestment
        
        capital = CapitalReinvestment()
        recommendations = capital.recommend_purchases()
        
        # Filter for items $500+ (need approval)
        pending = [r for r in recommendations if r["cost"] >= 500]
        return pending[:5]  # Top 5
    
    def get_intelligence_alerts(self):
        """Important signals from news/loophole scanners"""
        alerts = []
        
        # Check anomaly log
        anomaly_log = Path(__file__).parent.parent / "Logs" / "anomalies.log"
        if anomaly_log.exists():
            with open(anomaly_log, 'r') as f:
                lines = f.readlines()[-10:]  # Last 10
                for line in lines:
                    try:
                        alert = json.loads(line)
                        if alert.get("severity") == "HIGH":
                            alerts.append(alert)
                    except:
                        pass
        
        return alerts
    
    def generate_briefing(self):
        """Create full daily briefing"""
        from System.Finance.capital_reinvestment import CapitalReinvestment
        
        capital = CapitalReinvestment()
        total_revenue = capital.get_total_revenue()
        next_milestone = capital.get_next_milestone(total_revenue)
        
        overnight = self.get_overnight_activity()
        decisions = self.get_pending_decisions()
        alerts = self.get_intelligence_alerts()
        
        # Calculate overnight revenue
        overnight_revenue = sum([a["amount"] for a in overnight if a["amount"] > 0])
        
        briefing = {
            "date": datetime.now().isoformat(),
            "revenue": {
                "total": total_revenue,
                "overnight": overnight_revenue,
                "next_milestone": next_milestone
            },
            "overnight_activity": overnight,
            "pending_decisions": decisions,
            "intelligence_alerts": alerts
        }
        
        # Save to history
        filename = self.briefing_history / f"briefing_{datetime.now().strftime('%Y%m%d')}.json"
        with open(filename, 'w') as f:
            json.dump(briefing, f, indent=2)
        
        return briefing
    
    def print_briefing(self):
        """Display briefing in terminal"""
        briefing = self.generate_briefing()
        
        print("\n" + "="*60)
        print(f"📋 DAILY DIRECTOR BRIEFING - {datetime.now().strftime('%b %d, %Y')}")
        print("="*60)
        
        # Revenue status
        print(f"\n💰 REVENUE STATUS:")
        print(f"   Total: ${briefing['revenue']['total']:,.2f}")
        print(f"   Overnight: +${briefing['revenue']['overnight']:.2f}")
        
        if briefing['revenue']['next_milestone']['tier'] != "MAX":
            ms = briefing['revenue']['next_milestone']
            print(f"\n🎯 NEXT MILESTONE: {ms['tier']}")
            print(f"   Target: ${ms['threshold']:,}")
            print(f"   Progress: ${ms['progress']:,.2f} / ${ms['threshold']:,} ({ms['percent']:.1f}%)")
            print(f"   Remaining: ${ms['remaining']:,.2f}")
        else:
            print(f"\n🏆 ALL MILESTONES UNLOCKED!")
        
        # Overnight activity
        if briefing['overnight_activity']:
            print(f"\n📊 OVERNIGHT ACTIVITY ({len(briefing['overnight_activity'])} events):")
            
            # Group by source
            by_source = {}
            for activity in briefing['overnight_activity']:
                source = activity['source']
                if source not in by_source:
                    by_source[source] = []
                by_source[source].append(activity)
            
            for source, activities in by_source.items():
                total = sum([a['amount'] for a in activities])
                count = len(activities)
                print(f"   • {source}: {count} {'event' if count == 1 else 'events'} (${total:+.2f})")
        
        # Pending decisions
        if briefing['pending_decisions']:
            print(f"\n⚠️ DECISIONS NEEDED ({len(briefing['pending_decisions'])}):")
            for i, decision in enumerate(briefing['pending_decisions'], 1):
                print(f"\n   {i}. {decision['name']}")
                print(f"      Cost: ${decision['cost']:,}")
                if decision.get('roi_months', 0) > 0:
                    print(f"      ROI: {decision['roi_months']} months")
                print(f"      Approve purchase? [YES/NO]")
        
        # Intelligence alerts
        if briefing['intelligence_alerts']:
            print(f"\n🚨 INTELLIGENCE ALERTS ({len(briefing['intelligence_alerts'])}):")
            for alert in briefing['intelligence_alerts']:
                print(f"   • {alert.get('message', 'Alert')}")
                if alert.get('type') == "REVENUE_DROP":
                    print(f"     Action: Review Hydra monitor logs")
        
        print("\n" + "="*60)
        print("⏱️ Review complete. System operational.")
        print("="*60 + "\n")
        
        return briefing

if __name__ == "__main__":
    briefing = DirectorBriefing()
    briefing.print_briefing()
