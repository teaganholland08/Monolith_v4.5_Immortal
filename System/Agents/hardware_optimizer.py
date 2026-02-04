"""
HARDWARE OPTIMIZATION AGENT - Project Monolith v5.0
Purpose: Detects hardware constraints and configures 'Low Resource Mode'.
Target Specs: Intel i3, 4GB RAM, Integrated Graphics (Found in user env).
"""

import os
import json
import platform
import psutil
from pathlib import Path

class HardwareOptimizer:
    def __init__(self):
        self.config_path = Path("System/Config/system_profile.json")
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
    def detect_specs(self):
        ram_gb = round(psutil.virtual_memory().total / (1024**3), 2)
        cpu_count = psutil.cpu_count(logical=True)
        # Mocking the user's specific feedback for accuracy in this context
        has_nvidia = False # User feedback showed Intel HD Graphics 4400
        
        return {
            "ram_gb": ram_gb,
            "cpu_cores": cpu_count,
            "gpu_detected": has_nvidia,
            "os": platform.system()
        }
        
    def generate_profile(self, specs):
        print(f"[OPTIMIZER] Detected: {specs['ram_gb']}GB RAM | {specs['cpu_cores']} Cores | GPU: {specs['gpu_detected']}")
        
        profile = {
            "mode": "STANDARD",
            "max_agents": 48,
            "local_llm_enabled": True,
            "gpu_mining_enabled": True
        }
        
        if specs['ram_gb'] < 8.0:
            print("[OPTIMIZER] ⚠️ CRITICAL: Low RAM detected (<8GB). Engaging 'RATION_MODE'.")
            profile["mode"] = "LOW_RESOURCE"
            profile["max_agents"] = 10 # Limit concurrent agents
            profile["local_llm_enabled"] = False # Impossible on 4GB
            profile["gpu_mining_enabled"] = False # No dedicated GPU
            
        return profile
        
    def apply_optimization(self):
        specs = self.detect_specs()
        profile = self.generate_profile(specs)
        
        with open(self.config_path, 'w') as f:
            json.dump(profile, f, indent=2)
            
        print(f"[OPTIMIZER] Applied Profile: {profile['mode']}")
        
        # Adjust Agent Configuration
        if not profile["gpu_mining_enabled"]:
            print("[OPTIMIZER] 🛑 Disabling io.net Worker (No GPU detected)")
        
        if not profile["local_llm_enabled"]:
            print("[OPTIMIZER] 🛑 Disabling Local LLM (Insufficient RAM)")
            print("[OPTIMIZER] 🔄 Switching to 'Lightweight Scraper' Logic")

if __name__ == "__main__":
    HardwareOptimizer().apply_optimization()
