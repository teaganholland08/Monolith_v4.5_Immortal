"""
🎩 PROJECT MONOLITH: THE CONCIERGE
Your Personal Chief of Staff - Handles logistics, purchases, and scheduling
"""

import os
import sys
from datetime import datetime

# Add config path
sys.path.insert(0, 'C:/Monolith')

try:
    from config import CONFIG, is_local_mode, is_cloud_mode
    config_loaded = True
except ImportError:
    config_loaded = False

print("="*60)
print("🎩 THE CONCIERGE: PERSONAL ASSISTANT ACTIVE")
print("="*60)
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if config_loaded:
    print(f"Mode: {CONFIG['mode']}")
    print(f"AI Model: {CONFIG['llm_model']}")
print("="*60)

class ConciergeTools:
    """Tools for the personal assistant"""
    
    @staticmethod
    def search_local_vendors(query, location="Powell River, BC"):
        """Search for local vendors and services"""
        print(f"\n🔍 Searching for: {query} near {location}")
        # In production, this would use actual search APIs
        results = {
            "query": query,
            "location": location,
            "recommendations": [
                "Local Farm Co-op - Grass Fed Beef",
                "Powell River Butcher - Organic Meats",
                "BC Coastal Farms - Direct from Farm"
            ]
        }
        return results
    
    @staticmethod
    def check_supply_chain(region="British Columbia"):
        """Check for supply chain disruptions"""
        print(f"\n📊 Analyzing supply chain status for {region}")
        # In production, this would check real news APIs
        status = {
            "region": region,
            "status": "STABLE",
            "alerts": [],
            "recommendations": "No immediate concerns. Local supply chains operational."
        }
        return status
    
    @staticmethod
    def schedule_task(task, priority="MEDIUM"):
        """Add task to schedule"""
        print(f"\n📅 Scheduling: {task} (Priority: {priority})")
        return {
            "task": task,
            "priority": priority,
            "status": "QUEUED",
            "scheduled_for": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

def run_morning_briefing():
    """Execute the morning briefing routine"""
    print("\n" + "="*60)
    print("☀️ MORNING BRIEFING")
    print("="*60)
    
    # Check supply chain
    supply_status = ConciergeTools.check_supply_chain()
    print(f"\n✓ Supply Chain: {supply_status['status']}")
    print(f"  {supply_status['recommendations']}")
    
    # Find local vendors
    vendors = ConciergeTools.search_local_vendors("Grass Fed Beef")
    print(f"\n✓ Vendor Recommendations:")
    for vendor in vendors['recommendations']:
        print(f"  • {vendor}")
    
    print("\n" + "="*60)
    print("✅ BRIEFING COMPLETE")
    print("="*60)

def execute_command(user_command):
    """Execute a user command"""
    print(f"\n🎩 CONCIERGE PROCESSING: '{user_command}'")
    
    cmd = user_command.lower()
    
    # Route to appropriate tool
    if any(word in cmd for word in ['buy', 'order', 'purchase', 'find']):
        # Extract what they want to buy/find
        if 'beef' in cmd or 'meat' in cmd:
            return ConciergeTools.search_local_vendors("Grass Fed Beef")
        elif 'gym' in cmd or 'fitness' in cmd:
            return ConciergeTools.search_local_vendors("Gym")
        else:
            return ConciergeTools.search_local_vendors(user_command)
    
    elif any(word in cmd for word in ['schedule', 'remind', 'calendar']):
        return ConciergeTools.schedule_task(user_command)
    
    elif any(word in cmd for word in ['supply', 'chain', 'disruption']):
        return ConciergeTools.check_supply_chain()
    
    else:
        return {
            "status": "ACKNOWLEDGED",
            "message": f"Task delegated: {user_command}",
            "note": "Will process and report back."
        }

if __name__ == "__main__":
    # Run morning briefing as demo
    run_morning_briefing()
    
    print("\n\n" + "="*60)
    print("🎩 CONCIERGE READY FOR COMMANDS")
    print("="*60)
    print("Example: execute_command('Find me a gym in Powell River')")
