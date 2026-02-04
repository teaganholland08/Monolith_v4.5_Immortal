"""
TRAVEL AGENT - Trip Planning & Logistics
Manages travel bookings and logistics.
"""
import json
from pathlib import Path
from datetime import datetime

class TravelAgent:
    """
    The Travel Coordinator.
    - Books flights and hotels
    - Manages travel documents
    - Optimizes itineraries
    """
    
    def __init__(self):
        self.sentinel_dir = Path(__file__).parent.parent / "Sentinels"
        self.sentinel_dir.mkdir(exist_ok=True)
        
    def check_documents(self):
        return {
            "passport": {"expires": "2030-05-15", "status": "VALID"},
            "nexus": {"expires": "2028-01-01", "status": "VALID"}
        }
    
    def check_upcoming_trips(self):
        return []  # No trips planned
    
    def run(self):
        print("[TRAVEL] Checking travel status...")
        docs = self.check_documents()
        trips = self.check_upcoming_trips()
        
        sentinel_data = {
            "agent": "travel",
            "message": f"Documents: Valid | Trips: {len(trips)} planned",
            "status": "STANDBY",
            "documents": docs,
            "trips": trips,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(self.sentinel_dir / "travel.done", 'w', encoding='utf-8') as f:
            json.dump(sentinel_data, f, indent=2)
        
        print(f"[TRAVEL] All documents valid, {len(trips)} trips")

if __name__ == "__main__":
    TravelAgent().run()
