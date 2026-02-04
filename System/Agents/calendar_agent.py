"""
CALENDAR AGENT - Time & Schedule Management
Manages appointments, deadlines, and time optimization.
"""
import json
from pathlib import Path
from datetime import datetime, timedelta

class CalendarAgent:
    """
    The Time Manager.
    - Tracks appointments
    - Manages deadlines
    - Optimizes daily schedule
    """
    
    def __init__(self):
        self.sentinel_dir = Path(__file__).parent.parent / "Sentinels"
        self.sentinel_dir.mkdir(exist_ok=True)
        
    def get_today_events(self):
        return [
            {"time": "09:30", "event": "Director Briefing", "duration": 15},
            {"time": "14:00", "event": "Workshop Time", "duration": 180}
        ]
    
    def get_upcoming_deadlines(self):
        return [
            {"date": "2026-02-28", "task": "Q1 Tax Filing", "priority": "HIGH"},
            {"date": "2026-03-15", "task": "Insurance Renewal", "priority": "MEDIUM"}
        ]
    
    def run(self):
        print("[CALENDAR] Syncing schedule...")
        events = self.get_today_events()
        deadlines = self.get_upcoming_deadlines()
        
        sentinel_data = {
            "agent": "calendar",
            "message": f"Today: {len(events)} events | Deadlines: {len(deadlines)} upcoming",
            "status": "ACTIVE",
            "today_events": events,
            "deadlines": deadlines,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(self.sentinel_dir / "calendar.done", 'w', encoding='utf-8') as f:
            json.dump(sentinel_data, f, indent=2)
        
        print(f"[CALENDAR] {len(events)} events today")

if __name__ == "__main__":
    CalendarAgent().run()
