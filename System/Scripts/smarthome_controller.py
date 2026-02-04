"""
🏠 PROJECT MONOLITH: SMART HOME CONTROLLER
Universal IoT control via Home Assistant integration
"""

import os
import sys
import requests
from datetime import datetime

# Add config path
sys.path.insert(0, 'C:/Monolith')

print("="*60)
print("🏠 SMART HOME CONTROLLER ACTIVE")
print("="*60)

class SmartHomeController:
    """Universal smart home control interface"""
    
    def __init__(self):
        # Home Assistant configuration
        self.ha_url = os.getenv("HOME_ASSISTANT_URL", "http://homeassistant.local:8123")
        self.ha_token = os.getenv("HOME_ASSISTANT_TOKEN", "")
        self.simulation_mode = not self.ha_token  # Use simulation if no token
        
        if self.simulation_mode:
            print("⚠️  SIMULATION MODE: No Home Assistant token found")
            print("   Set HOME_ASSISTANT_TOKEN to enable real control")
        else:
            print(f"✓ Connected to: {self.ha_url}")
    
    def control_device(self, device_name, command, value=None):
        """
        Control any smart device
        
        Args:
            device_name: Name of device (e.g., "Office Light", "Front Door")
            command: Action to perform (e.g., "on", "off", "lock", "unlock", "set")
            value: Optional value for commands like "set temperature to 72"
        """
        print(f"\n🎯 COMMAND: {device_name} → {command.upper()}")
        
        if self.simulation_mode:
            # Simulation mode - just log the action
            result = {
                "device": device_name,
                "command": command,
                "value": value,
                "status": "SIMULATED",
                "message": f"✓ {device_name} would be set to {command}"
            }
            print(f"   ✓ SIMULATION: {device_name} → {command}")
            if value:
                print(f"   Value: {value}")
        else:
            # Real mode - send to Home Assistant
            try:
                # Construct Home Assistant API call
                headers = {
                    "Authorization": f"Bearer {self.ha_token}",
                    "Content-Type": "application/json"
                }
                
                # Map command to Home Assistant service
                service_map = {
                    "on": "turn_on",
                    "off": "turn_off",
                    "lock": "lock",
                    "unlock": "unlock",
                    "open": "open_cover",
                    "close": "close_cover"
                }
                
                service = service_map.get(command.lower(), "turn_on")
                
                payload = {
                    "entity_id": self._get_entity_id(device_name)
                }
                
                if value:
                    payload["value"] = value
                
                response = requests.post(
                    f"{self.ha_url}/api/services/homeassistant/{service}",
                    headers=headers,
                    json=payload,
                    timeout=5
                )
                
                result = {
                    "device": device_name,
                    "command": command,
                    "status": "SUCCESS" if response.ok else "FAILED",
                    "message": f"✓ {device_name} {command} executed"
                }
                
            except Exception as e:
                result = {
                    "device": device_name,
                    "command": command,
                    "status": "ERROR",
                    "message": f"Error: {str(e)}"
                }
        
        return result
    
    def _get_entity_id(self, device_name):
        """Convert friendly name to Home Assistant entity ID"""
        # Simple conversion - in production, this would query HA for actual entity IDs
        name_lower = device_name.lower().replace(" ", "_")
        
        if "light" in name_lower:
            return f"light.{name_lower}"
        elif "lock" in name_lower or "door" in name_lower:
            return f"lock.{name_lower}"
        elif "switch" in name_lower:
            return f"switch.{name_lower}"
        elif "climate" in name_lower or "thermostat" in name_lower:
            return f"climate.{name_lower}"
        else:
            return f"switch.{name_lower}"
    
    def get_status(self, device_name):
        """Get current status of a device"""
        print(f"\n📊 Checking status: {device_name}")
        
        if self.simulation_mode:
            return {
                "device": device_name,
                "state": "unknown",
                "mode": "simulation"
            }
        else:
            # Query Home Assistant for actual status
            try:
                headers = {
                    "Authorization": f"Bearer {self.ha_token}",
                    "Content-Type": "application/json"
                }
                
                entity_id = self._get_entity_id(device_name)
                response = requests.get(
                    f"{self.ha_url}/api/states/{entity_id}",
                    headers=headers,
                    timeout=5
                )
                
                if response.ok:
                    data = response.json()
                    return {
                        "device": device_name,
                        "state": data.get("state"),
                        "attributes": data.get("attributes", {})
                    }
            except Exception as e:
                return {
                    "device": device_name,
                    "error": str(e)
                }

# Global controller instance
controller = SmartHomeController()

def execute_home_command(user_input):
    """Parse and execute a natural language home command"""
    print(f"\n🏠 PROCESSING: '{user_input}'")
    
    cmd = user_input.lower()
    
    # Parse the command
    if "light" in cmd:
        device = "Office Light" if "office" in cmd else "Living Room Light"
        command = "on" if "on" in cmd else "off"
        return controller.control_device(device, command)
    
    elif "door" in cmd or "lock" in cmd:
        device = "Front Door"
        command = "lock" if "lock" in cmd else "unlock"
        return controller.control_device(device, command)
    
    elif "temperature" in cmd or "thermostat" in cmd or "heat" in cmd or "cool" in cmd:
        device = "Thermostat"
        if "set" in cmd:
            # Extract temperature value
            import re
            temp_match = re.search(r'\d+', cmd)
            value = temp_match.group() if temp_match else "72"
            return controller.control_device(device, "set", value)
        else:
            command = "on" if any(word in cmd for word in ["heat", "warm", "on"]) else "off"
            return controller.control_device(device, command)
    
    else:
        return {
            "status": "UNKNOWN_COMMAND",
            "message": f"Could not parse command: {user_input}",
            "suggestion": "Try: 'Turn on office lights' or 'Lock the front door'"
        }

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🏠 SMART HOME CONTROLLER READY")
    print("="*60)
    print("\nExample commands:")
    print("  • execute_home_command('Turn on the office lights')")
    print("  • execute_home_command('Lock the front door')")
    print("  • execute_home_command('Set temperature to 72')")
    print("\n" + "="*60)
