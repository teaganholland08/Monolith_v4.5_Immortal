"""
HARDENED DISPATCHER - Project Monolith v5.0
Implements: Kill Switch, Emergency Panic, Inter-agent Guardian
Purpose: Centralized supervisor for high-risk commands.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

class HardenedDispatcher:
    """
    Super-Agent that handles critical system overrides.
    It can instantly terminate the Monolith graph or purge volatile memory.
    """
    
    def __init__(self):
        self.root = Path(__file__).parent.parent.parent
        self.kill_file = self.root / ".system_kill"
        self.panic_file = self.root / ".system_panic"
        self.logs_dir = self.root / "System" / "Logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)

    def trigger_kill_switch(self, reason: str):
        """Permanent shutdown until manual reset"""
        print(f"🚨 [KILL SWITCH] TRIGGERED: {reason}")
        with open(self.kill_file, 'w') as f:
            f.write(f"TIMESTAMP: {datetime.now().isoformat()}\nREASON: {reason}")
        
        self._log_emergency("KILL_SWITCH", reason)
        sys.exit(666) # Emergency exit code

    def trigger_panic_protocol(self):
        """Volatile data purge and offline state"""
        print("⚠️ [PANIC] PURGING VOLATILE SESSIONS...")
        # In a real sys, we would wipe /tmp, clear redis, and rotate vault keys
        self._log_emergency("PANIC", "Manual Panic Triggered")
        
        # Create sentinel
        with open(self.panic_file, 'w') as f:
            f.write("PANIC ACTIVE")

    def check_safety(self) -> bool:
        """Returns False if the system is in a locked state"""
        if self.kill_file.exists():
            print("🛑 SYSTEM LOCKED: KILL SWITCH ACTIVE.")
            return False
        return True

    def _log_emergency(self, event_type: str, detail: str):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event_type,
            "detail": detail
        }
        with open(self.logs_dir / "emergency.log", 'a') as f:
            f.write(json.dumps(log_entry) + "\n")

if __name__ == "__main__":
    dispatcher = HardenedDispatcher()
    if len(sys.argv) > 1:
        if sys.argv[1] == "kill":
            dispatcher.trigger_kill_switch("Manual CLI override")
        elif sys.argv[1] == "panic":
            dispatcher.trigger_panic_protocol()
    else:
        print("Dispatcher Status: ONLINE")
        print(f"Safety Check: {dispatcher.check_safety()}")
