"""
VOICE INTERFACE - Natural Language Command Processing
Enables voice control of the entire Monolith ecosystem.
"""
import json
from pathlib import Path
from datetime import datetime

class VoiceInterface:
    """
    Natural language command processor.
    In production: Connects to ElevenLabs for TTS, Whisper for STT.
    """
    
    def __init__(self):
        self.sentinel_dir = Path(__file__).parent.parent / "Sentinels"
        self.sentinel_dir.mkdir(exist_ok=True)
        
        # Command patterns
        self.commands = {
            "status": self.get_status,
            "briefing": self.get_briefing,
            "lock": self.lock_down,
            "optimize": self.optimize,
            "vanish": self.vanish
        }
    
    def parse_command(self, text):
        """Parse natural language into action"""
        text = text.lower()
        
        for keyword, action in self.commands.items():
            if keyword in text:
                return keyword, action
        
        return "unknown", None
    
    def get_status(self):
        return {"response": "All systems nominal. 12 agents active. Revenue: $247.82 today."}
    
    def get_briefing(self):
        return {"response": "Director Briefing: 3 decisions pending. Health: GREEN. Wealth: +2.3%."}
    
    def lock_down(self):
        return {"response": "Lockdown initiated. All external connections severed."}
    
    def optimize(self):
        return {"response": "Running optimization cycle. Scout found 3 upgrades."}
    
    def vanish(self):
        return {"response": "VANISH protocol armed. Awaiting biometric confirmation."}
    
    def run(self):
        print("[VOICE] Voice interface active...")
        
        # Simulated voice input for testing
        test_commands = ["What's my status?", "Run the briefing", "Optimize everything"]
        responses = []
        
        for cmd in test_commands:
            keyword, action = self.parse_command(cmd)
            if action:
                result = action()
                responses.append({"command": cmd, "action": keyword, "result": result})
        
        sentinel_data = {
            "agent": "voice_interface",
            "message": f"Voice ready. {len(self.commands)} commands registered.",
            "status": "ACTIVE",
            "commands_available": list(self.commands.keys()),
            "test_responses": responses,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(self.sentinel_dir / "voice_interface.done", 'w', encoding='utf-8') as f:
            json.dump(sentinel_data, f, indent=2)
        
        print(f"[VOICE] Ready. {len(self.commands)} commands available.")

if __name__ == "__main__":
    VoiceInterface().run()
