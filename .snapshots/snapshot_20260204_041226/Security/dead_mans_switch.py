"""
MONOLITH DEAD MAN'S SWITCH
Auto-wipes sensitive data if you don't check in for 7 days

Usage:
  python dead_mans_switch.py           # Run monitor in background
  python dead_mans_switch.py checkin   # Manual check-in (resets timer)

Integration:
  Add to monolith_omega.py shadow_loop for auto-monitoring
"""

import time
import os
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

class DeadMansSwitch:
    def __init__(self, days_threshold=7):
        self.checkin_file = Path(__file__).parent / ".last_checkin"
        self.days_threshold = days_threshold
        self.panic_script = Path(__file__).parent.parent.parent / "PANIC_BUTTON.bat"
        
    def check_in(self):
        """Manual check-in - resets the timer"""
        with open(self.checkin_file, 'w') as f:
            f.write(datetime.now().isoformat())
        print(f"✓ CHECK-IN RECORDED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Next check-in required before: {(datetime.now() + timedelta(days=self.days_threshold)).strftime('%Y-%m-%d')}")
        return True
    
    def days_since_checkin(self):
        """Calculate days since last check-in"""
        if not self.checkin_file.exists():
            self.check_in()  # First run
            return 0
        
        try:
            with open(self.checkin_file, 'r') as f:
                last_checkin = datetime.fromisoformat(f.read().strip())
            
            delta = datetime.now() - last_checkin
            return delta.days
        except Exception as e:
            print(f"⚠️ Error reading check-in file: {e}")
            return 0
    
    def trigger_panic(self):
        """Execute panic protocol"""
        print("\n" + "="*60)
        print("🚨 DEAD MAN'S SWITCH TRIGGERED 🚨")
        print("="*60)
        print(f"\nNo check-in detected for {self.days_threshold}+ days.")
        print("Assuming compromise or incapacitation.")
        print("\nInitiating PANIC PROTOCOL in 30 seconds...")
        print("Press CTRL+C to abort if this is a false alarm.")
        print("="*60 + "\n")
        
        try:
            time.sleep(30)
            
            # Execute panic button
            if self.panic_script.exists():
                subprocess.run([str(self.panic_script)], shell=True)
                print("\n✓ PANIC PROTOCOL COMPLETE")
            else:
                print(f"\n⚠️ PANIC SCRIPT NOT FOUND: {self.panic_script}")
                print("Manual wipe required.")
                
        except KeyboardInterrupt:
            print("\n\n⚠️ ABORT: User intervention detected")
            print("Dead Man's Switch cancelled.")
            self.check_in()  # Auto check-in on abort
    
    def monitor(self, check_interval_hours=24):
        """Continuous monitoring - run in background"""
        print("🔐 DEAD MAN'S SWITCH: MONITORING ACTIVE")
        print(f"   Threshold: {self.days_threshold} days")
        print(f"   Check interval: {check_interval_hours} hours")
        print(f"   Last check-in: {self.checkin_file.exists() and 'Found' or 'Never'}")
        
        if not self.checkin_file.exists():
            self.check_in()
        
        cycle = 0
        while True:
            days = self.days_since_checkin()
            
            # Status update every 24 hours
            if cycle % 24 == 0:
                print(f"\n📍 STATUS: Days since check-in: {days}/{self.days_threshold}")
                
                if days >= self.days_threshold - 2:
                    print(f"   ⚠️ WARNING: Only {self.days_threshold - days} days until trigger!")
            
            # Trigger panic if threshold exceeded
            if days >= self.days_threshold:
                self.trigger_panic()
                break  # Exit after panic (system will be wiped)
            
            # Wait for next check
            time.sleep(check_interval_hours * 3600)
            cycle += 1
    
    def status(self):
        """Show current status"""
        days = self.days_since_checkin()
        remaining = self.days_threshold - days
        
        print("\n🔐 DEAD MAN'S SWITCH STATUS")
        print("="*60)
        
        if not self.checkin_file.exists():
            print("Status: NOT INITIALIZED")
            print("Action: Run 'python dead_mans_switch.py checkin' to start")
        else:
            with open(self.checkin_file, 'r') as f:
                last = datetime.fromisoformat(f.read().strip())
            
            print(f"Last Check-in: {last.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Days Since:    {days}")
            print(f"Days Until:    {remaining}")
            
            if remaining <= 0:
                print("\n🚨 STATUS: TRIGGER IMMINENT")
            elif remaining <= 2:
                print(f"\n⚠️ STATUS: WARNING (check in within {remaining} days)")
            else:
                print(f"\n✓ STATUS: SAFE ({remaining} days remaining)")
        
        print("="*60 + "\n")

if __name__ == "__main__":
    import sys
    
    switch = DeadMansSwitch(days_threshold=7)
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "checkin":
            switch.check_in()
        
        elif command == "status":
            switch.status()
        
        elif command == "test":
            # Test mode - set threshold to 0 days
            print("⚠️ TEST MODE: Threshold set to 0 days")
            switch.days_threshold = 0
            switch.monitor(check_interval_hours=0.01)  # Check every 36 seconds
        
        else:
            print(f"Unknown command: {command}")
            print("\nUsage:")
            print("  python dead_mans_switch.py           # Run monitor")
            print("  python dead_mans_switch.py checkin   # Manual check-in")
            print("  python dead_mans_switch.py status    # Show status")
            print("  python dead_mans_switch.py test      # Test trigger")
    
    else:
        # Default: run monitor
        switch.monitor()
