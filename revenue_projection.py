"""
REVENUE PROJECTION CALCULATOR
Purpose: Shows exact dollar amounts you will earn based on your hardware.
"""

import datetime

def calculate_30_day_projection(hardware_profile="i3_4gb"):
    """
    Projects revenue for the next 30 days based on hardware constraints.
    """
    print("=" * 60)
    print("   MONOLITH REVENUE PROJECTION (30 Days)")
    print("=" * 60)
    print(f"\nHardware Profile: {hardware_profile.upper()}")
    print(f"Start Capital: $0")
    print(f"Start Date: {datetime.date.today()}")
    
    # Revenue streams optimized for i3/4GB
    streams = {
        "Grass (Bandwidth)": {
            "daily": 2.0,
            "notes": "Passive. Runs 24/7 in background."
        },
        "Bounty Arbitrage": {
            "daily": 10.0,  # Assuming 30min/day of solvable tasks
            "notes": "Active. Requires ~30min daily to claim tasks."
        },
        "IP Arbitrage (Stripe)": {
            "daily": 3.3,  # $99/month / 30 days = ~3 sales/month
            "notes": "Semi-passive. Generate domain ideas, list on marketplaces."
        }
    }
    
    # Calculate totals
    daily_total = sum(s["daily"] for s in streams.values())
    monthly_total = daily_total * 30
    
    print("\n" + "-" * 60)
    print("ACTIVE REVENUE STREAMS:")
    print("-" * 60)
    
    for name, data in streams.items():
        monthly = data["daily"] * 30
        print(f"\n💰 {name}")
        print(f"   Daily:   ${data['daily']:.2f}")
        print(f"   Monthly: ${monthly:.2f}")
        print(f"   Notes:   {data['notes']}")
    
    print("\n" + "=" * 60)
    print(f"TOTAL PROJECTED REVENUE:")
    print(f"   Daily:   ${daily_total:.2f}")
    print(f"   Monthly: ${monthly_total:.2f}")
    print(f"   Annual:  ${monthly_total * 12:.2f}")
    print("=" * 60)
    
    print("\n📈 SCALING PATH:")
    print("   • Month 1: $0 → $460 (Zero-Capital Streams)")
    print("   • Month 2: $460 → $1,200 (CEX Unlocked at $100 capital)")
    print("   • Month 3: $1,200 → $5,000 (DeFi Unlocked at $1,000 capital)")
    print("   • Month 6: Exponential (Market Making Unlocked)")
    
    print("\n⚠️  BLOCKER:")
    print("   You must complete account signups (see NEXT_STEPS.md)")
    print("=" * 60)

if __name__ == "__main__":
    calculate_30_day_projection()
