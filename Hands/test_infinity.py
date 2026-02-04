"""
TEST: INFINITE CAPABILITY (Moltbot Proof of Concept)
Purpose: Verify that our custom engine can drive a browser and see the world.
"""
import sys
import os

# Create dynamic path to find modules
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import config
# Force simulation mode OFF to test real browser
config.USE_SIMULATION_MODE = False

from Hands.moltbot import Moltbot

def test_infinity():
    print("🚀 INITIATING ANTIGRAVITY LINK...")
    
    # 1. Initialize our custom engine
    bot = Moltbot(headless=True)
    
    # 2. Assign a mission (Visit a real site)
    target = "https://www.example.com"
    print(f"🌍 FLYING TO: {target}")
    
    # 3. Execute
    html = bot.browse(target)
    
    # 4. Extract Intel
    print(f"👀 VISUAL: Page size is {len(html)} bytes")
    
    # 5. Verify Content
    if "Example Domain" in html:
        print("✅ SUCCESS: Target Identified. We can read the web.")
    else:
        print("❌ FAILURE: Vision obscured.")
        
    bot.close()
    print("🏁 MISSION COMPLETE. We have our own automation engine.")

if __name__ == "__main__":
    test_infinity()
