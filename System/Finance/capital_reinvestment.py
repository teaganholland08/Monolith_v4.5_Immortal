"""
MONOLITH CAPITAL REINVESTMENT ENGINE
Autonomous hardware purchasing based on revenue milestones

Strategy: "Remember everything, buy as needed when it makes more money"

Flow:
1. Monitor revenue from all sources (Gumroad, Medium, Crypto)
2. Track progress toward hardware milestones
3. Auto-generate purchase recommendations
4. (Optional) Auto-purchase via API when enabled

Tiers:
- Tier 1 ($2,000): Energy efficiency (saves money)
- Tier 2 ($5,000): Premium appliances (saves time)
- Tier 3 ($10,000): Security fortress (protects assets)
- Tier 4 ($25,000): Full automation (robotics, AI)
"""

import sqlite3
from datetime import datetime
from pathlib import Path
import json

class CapitalReinvestment:
    def __init__(self):
        self.ledger_db = Path(__file__).parent.parent / "Logs" / "ledger.db"
        self.purchases_db = Path(__file__).parent.parent / "Logs" / "purchases.db"
        self.config_file = Path(__file__).parent.parent / "Config" / "reinvestment_config.json"
        
        # Hardware purchase tiers
        self.tiers = {
            "TIER_1_EFFICIENCY": {
                "threshold": 2000,
                "name": "Energy Efficiency & Infrastructure",
                "goal": "Save $500/month on utilities",
                "items": [
                    {
                        "name": "Home Energy Monitor (Sense)",
                        "cost": 299,
                        "roi_months": 6,
                        "savings_per_month": 50,
                        "priority": 1,
                        "url": "https://sense.com"
                    },
                    {
                        "name": "Ecobee Smart Thermostat Premium",
                        "cost": 249,
                        "roi_months": 12,
                        "savings_per_month": 25,
                        "priority": 2,
                        "url": "https://ecobee.com"
                    },
                    {
                        "name": "Home Assistant Yellow",
                        "cost": 179,
                        "roi_months": 0,  # Infrastructure
                        "savings_per_month": 0,
                        "priority": 1,
                        "url": "https://home-assistant.io"
                    }
                ]
            },
            "TIER_2_CONVENIENCE": {
                "threshold": 5000,
                "name": "Bespoke AI Life (Premium Appliances)",
                "goal": "Save 10+ hours/week on chores",
                "items": [
                    {
                        "name": "Samsung Bespoke AI Laundry Combo",
                        "cost": 3499,
                        "roi_months": 0,  # Quality of life
                        "time_saved_hours_week": 5,
                        "priority": 1,
                        "url": "https://samsung.com/bespoke"
                    },
                    {
                        "name": "Samsung Jet Bot AI+ (Vacuum/Mop)",
                        "cost": 799,
                        "roi_months": 0,
                        "time_saved_hours_week": 3,
                        "priority": 2,
                        "url": "https://samsung.com/jetbot"
                    },
                    {
                        "name": "Samsung Bespoke 4-Door Refrigerator (AI Vision)",
                        "cost": 4599,
                        "roi_months": 24,  # Reduces food waste
                        "savings_per_month": 75,
                        "priority": 3,
                        "url": "https://samsung.com/bespoke"
                    }
                ]
            },
            "TIER_3_FORTRESS": {
                "threshold": 10000,
                "name": "Total Security & Resilience",
                "goal": "Protect high-value assets",
                "items": [
                    {
                        "name": "Ubiquiti Dream Machine SE + Cameras (4K)",
                        "cost": 2499,
                        "roi_months": 0,  # Security
                        "priority": 1,
                        "url": "https://store.ui.com"
                    },
                    {
                        "name": "Starlink Mini (Backup Internet)",
                        "cost": 599,
                        "recurring": 50,  # per month
                        "priority": 2,
                        "url": "https://starlink.com"
                    },
                    {
                        "name": "Meshtastic Relay Network (5 nodes)",
                        "cost": 250,
                        "roi_months": 0,
                        "priority": 3,
                        "url": "https://meshtastic.org"
                    }
                ]
            },
            "TIER_4_AUTOMATION": {
                "threshold": 25000,
                "name": "Full Robotics & AI Assistant",
                "goal": "Achieve 95% household automation",
                "items": [
                    {
                        "name": "Samsung Bespoke AI WindFree HVAC",
                        "cost": 8999,
                        "roi_months": 48,
                        "savings_per_month": 150,
                        "priority": 1,
                        "url": "https://samsung.com/bespoke"
                    },
                    {
                        "name": "RTX 5090 (AI Workstation Upgrade)",
                        "cost": 2499,
                        "roi_months": 3,  # Faster Genesis output
                        "priority": 2,
                        "url": "https://nvidia.com"
                    },
                    {
                        "name": "Google Pixel 9 Pro + GrapheneOS",
                        "cost": 999,
                        "roi_months": 0,  # Security
                        "priority": 3,
                        "url": "https://grapheneos.org"
                    }
                ]
            }
        }
        
        self._init_purchases_db()
    
    def _init_purchases_db(self):
        """Create purchases tracking database"""
        self.purchases_db.parent.mkdir(exist_ok=True)
        
        conn = sqlite3.connect(self.purchases_db)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS purchase_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tier TEXT NOT NULL,
                item_name TEXT NOT NULL,
                cost REAL NOT NULL,
                priority INTEGER NOT NULL,
                status TEXT DEFAULT 'PENDING',
                added_date TEXT NOT NULL,
                purchased_date TEXT,
                url TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL,
                purchase_date TEXT NOT NULL,
                cost REAL NOT NULL,
                tier TEXT NOT NULL,
                monthly_savings REAL DEFAULT 0,
                notes TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def get_total_revenue(self):
        """Get all-time revenue from ledger"""
        if not self.ledger_db.exists():
            return 0
        
        conn = sqlite3.connect(self.ledger_db)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0) 
            FROM transactions 
            WHERE type = 'REVENUE'
        """)
        
        total = cursor.fetchone()[0]
        conn.close()
        return total
    
    def get_current_tier(self, total_revenue):
        """Determine highest unlocked tier"""
        unlocked = None
        
        for tier_key in sorted(self.tiers.keys()):
            if total_revenue >= self.tiers[tier_key]["threshold"]:
                unlocked = tier_key
        
        return unlocked
    
    def get_next_milestone(self, total_revenue):
        """Get next revenue milestone"""
        for tier_key in sorted(self.tiers.keys()):
            threshold = self.tiers[tier_key]["threshold"]
            if total_revenue < threshold:
                return {
                    "tier": tier_key,
                    "threshold": threshold,
                    "progress": total_revenue,
                    "remaining": threshold - total_revenue,
                    "percent": (total_revenue / threshold) * 100
                }
        
        # All tiers unlocked
        return {
            "tier": "MAX",
            "threshold": 25000,
            "progress": total_revenue,
            "remaining": 0,
            "percent": 100
        }
    
    def recommend_purchases(self):
        """Generate purchase recommendations based on current revenue"""
        total_revenue = self.get_total_revenue()
        current_tier = self.get_current_tier(total_revenue)
        
        recommendations = []
        
        if current_tier:
            tier_data = self.tiers[current_tier]
            
            for item in tier_data["items"]:
                # Check if already purchased
                conn = sqlite3.connect(self.purchases_db)
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT COUNT(*) FROM inventory 
                    WHERE item_name = ?
                """, (item["name"],))
                
                already_owned = cursor.fetchone()[0] > 0
                conn.close()
                
                if not already_owned:
                    recommendations.append({
                        "tier": current_tier,
                        "tier_name": tier_data["name"],
                        **item
                    })
        
        # Sort by priority
        recommendations.sort(key=lambda x: x["priority"])
        return recommendations
    
    def add_to_queue(self, item):
        """Add item to purchase queue"""
        conn = sqlite3.connect(self.purchases_db)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO purchase_queue 
            (tier, item_name, cost, priority, added_date, url)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            item["tier"],
            item["name"],
            item["cost"],
            item["priority"],
            datetime.now().isoformat(),
            item.get("url", "")
        ))
        
        conn.commit()
        conn.close()
        
        print(f"✓ Added to queue: {item['name']} (${item['cost']})")
    
    def mark_purchased(self, item_name):
        """Mark item as purchased and add to inventory"""
        conn = sqlite3.connect(self.purchases_db)
        cursor = conn.cursor()
        
        # Get item details from queue
        cursor.execute("""
            SELECT tier, cost FROM purchase_queue 
            WHERE item_name = ? AND status = 'PENDING'
        """, (item_name,))
        
        result = cursor.fetchone()
        if not result:
            print(f"⚠️ Item not found in queue: {item_name}")
            conn.close()
            return
        
        tier, cost = result
        
        # Update queue status
        cursor.execute("""
            UPDATE purchase_queue 
            SET status = 'PURCHASED', purchased_date = ?
            WHERE item_name = ?
        """, (datetime.now().isoformat(), item_name))
        
        # Add to inventory
        cursor.execute("""
            INSERT INTO inventory 
            (item_name, purchase_date, cost, tier, notes)
            VALUES (?, ?, ?, ?, ?)
        """, (
            item_name,
            datetime.now().isoformat(),
            cost,
            tier,
            "Auto-purchased by Monolith"
        ))
        
        conn.commit()
        conn.close()
        
        print(f"✓ Marked as purchased: {item_name}")
    
    def generate_report(self):
        """Generate full capital reinvestment report"""
        total_revenue = self.get_total_revenue()
        next_milestone = self.get_next_milestone(total_revenue)
        recommendations = self.recommend_purchases()
        
        print("\n" + "="*60)
        print("💰 CAPITAL REINVESTMENT ENGINE - STATUS REPORT")
        print("="*60)
        
        print(f"\n📊 REVENUE STATUS:")
        print(f"   Total Generated: ${total_revenue:,.2f}")
        
        if next_milestone["tier"] != "MAX":
            print(f"\n🎯 NEXT MILESTONE: {self.tiers[next_milestone['tier']]['name']}")
            print(f"   Target: ${next_milestone['threshold']:,}")
            print(f"   Progress: ${next_milestone['progress']:,.2f} / ${next_milestone['threshold']:,}")
            print(f"   Completion: {next_milestone['percent']:.1f}%")
            print(f"   Remaining: ${next_milestone['remaining']:,.2f}")
        else:
            print(f"\n🏆 ALL MILESTONES UNLOCKED!")
        
        if recommendations:
            print(f"\n🛒 RECOMMENDED PURCHASES ({len(recommendations)} items):")
            for rec in recommendations[:5]:  # Top 5
                print(f"\n   {rec['priority']}. {rec['name']}")
                print(f"      Cost: ${rec['cost']:,}")
                if rec.get('roi_months', 0) > 0:
                    print(f"      ROI: {rec['roi_months']} months")
                if rec.get('savings_per_month', 0) > 0:
                    print(f"      Saves: ${rec['savings_per_month']}/month")
                if rec.get('time_saved_hours_week', 0) > 0:
                    print(f"      Time Saved: {rec['time_saved_hours_week']} hrs/week")
                print(f"      URL: {rec['url']}")
        else:
            print("\n   No recommendations at this revenue level.")
        
        # Show inventory
        conn = sqlite3.connect(self.purchases_db)
        cursor = conn.cursor()
        cursor.execute("SELECT item_name, cost FROM inventory")
        inventory = cursor.fetchall()
        conn.close()
        
        if inventory:
            print(f"\n📦 CURRENT INVENTORY ({len(inventory)} items):")
            total_invested = sum([item[1] for item in inventory])
            for item_name, cost in inventory:
                print(f"   • {item_name} (${cost:,})")
            print(f"\n   Total Invested: ${total_invested:,.2f}")
        
        print("\n" + "="*60 + "\n")
        
        return {
            "total_revenue": total_revenue,
            "next_milestone": next_milestone,
            "recommendations": recommendations,
            "inventory": inventory
        }

if __name__ == "__main__":
    engine = CapitalReinvestment()
    engine.generate_report()
