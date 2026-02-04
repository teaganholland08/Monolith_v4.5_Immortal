"""
ADAPTIVE COMPUTE ENGINE (Meta-ACE) - Project Monolith v5.1
Purpose: Dynamic task profiling and compute allocation.
Strategy: Optimize for 4GB RAM by offloading heavy tasks to cloud/remote when local resources are constrained.
"""

import json
import psutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

class AdaptiveComputeEngine:
    """
    The "Brain of the Brain".
    Allocates compute resources based on real-time hardware telemetry.
    """
    def __init__(self):
        self.root = Path(__file__).parent.parent.parent
        self.config_dir = self.root / "System" / "Config"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.state_file = self.config_dir / "ace_state.json"
        
    def profile_task(self, task_metadata: Dict[str, Any]) -> str:
        """
        Analyzes a task and returns the optimal execution target.
        Targets: "LOCAL_LOW", "LOCAL_HIGH", "CLOUD_REMOTE", "DEFERRED"
        """
        ram_gb = psutil.virtual_memory().total / (1024**3)
        available_ram = psutil.virtual_memory().available / (1024**3)
        task_weight = task_metadata.get("weight", "MEDIUM")
        
        # 4GB RAM constraint logic (The user's specific hardware)
        if ram_gb <= 4.1:
            if task_weight == "HIGH" or available_ram < 0.5:
                return "CLOUD_REMOTE"
            return "LOCAL_LOW"
        
        return "LOCAL_HIGH"

    def update_resource_map(self):
        """Monitors system-wide resource usage and updates ACE state."""
        state = {
            "timestamp": datetime.now().isoformat(),
            "available_ram": round(psutil.virtual_memory().available / (1024**3), 2),
            "cpu_load": psutil.cpu_percent(),
            "ace_strategy": "RATION_CONSOLIDATED" if psutil.virtual_memory().total / (1024**3) < 8 else "PERFORMANCE"
        }
        
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)
            
        return state

    def run(self):
        print("[META-ACE] 🧠 Optimizing Compute Architecture for i3/4GB Hardware...")
        state = self.update_resource_map()
        print(f"[META-ACE] Strategy: {state['ace_strategy']} | Available RAM: {state['available_ram']}GB")

if __name__ == "__main__":
    ace = AdaptiveComputeEngine()
    ace.run()
