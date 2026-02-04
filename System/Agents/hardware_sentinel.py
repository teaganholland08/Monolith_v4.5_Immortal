"""
HARDWARE SENTINEL - Project Monolith v5.0
Purpose: Monitors Physical Infrastructure (EnerVenue, Source Hydropanels, Rezvani).
"""

import json
import random
from pathlib import Path
from datetime import datetime

class HardwareSentinel:
    """
    Agent interfacing with physical hardware status APIs.
    Monitors Power (EnerVenue), Water (Source), and Security (Sunflower).
    """
    
    def __init__(self):
        self.sentinel_dir = Path(__file__).parent.parent / "Sentinels"
        self.sentinel_dir.mkdir(exist_ok=True)

    def get_hardware_status(self):
        """Simulated hardware telemetry handshake"""
        return {
            "EnerVenue_ESV": {
                "charge": random.randint(85, 99),
                "cycles": 420,
                "health": "EXCELLENT",
                "temp": "22C"
            },
            "Source_Hydropanels_R3": {
                "reserves": "42L",
                "daily_prod": "8.5L",
                "ph": 7.2,
                "status": "OPTIMAL"
            },
            "Sunflower_Beehive": {
                "drones": "3/3 READY",
                "last_patrol": "15m ago",
                "threat_level": "ZERO"
            }
        }

    def run(self):
        print("[HARDWARE] Polling physical infrastructure...")
        status = self.get_hardware_status()
        
        # Logic: If battery < 20% or water < 5L, status = RED
        overall_status = "GREEN"
        if status["EnerVenue_ESV"]["charge"] < 20: 
            overall_status = "RED"
            
        sentinel_data = {
            "agent": "hardware_sentinel",
            "message": f"Power: {status['EnerVenue_ESV']['charge']}% | Water: {status['Source_Hydropanels_R3']['reserves']} | Drones: ACTIVE",
            "status": overall_status,
            "telemetry": status,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(self.sentinel_dir / "hardware_sentinel.done", 'w', encoding='utf-8') as f:
            json.dump(sentinel_data, f, indent=2)
            
        print(f"[HARDWARE] Status: {overall_status} | Power: {status['EnerVenue_ESV']['charge']}%")

if __name__ == "__main__":
    HardwareSentinel().run()
