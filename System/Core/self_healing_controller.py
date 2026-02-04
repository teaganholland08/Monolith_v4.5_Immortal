"""
SELF-HEALING CONTROLLER - Best-in-World 2026 Standard
Implements: Causal Memory, Circuit Breaker, Exponential Backoff, Auto-Restart
Purpose: Ensure system resilience and automatic recovery from failures.
"""

import json
import time
import threading
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Callable, Optional, Any
from enum import Enum
import functools

# --- Configuration ---
MEMORY_DIR = Path(__file__).parent.parent.parent / "Brain" / "Memory"
MEMORY_DIR.mkdir(parents=True, exist_ok=True)


class CircuitState(Enum):
    CLOSED = "CLOSED"      # Normal operation
    OPEN = "OPEN"          # Failing, rejecting calls
    HALF_OPEN = "HALF_OPEN"  # Testing recovery


@dataclass
class FailureRecord:
    """Record of a failure and its resolution"""
    component: str
    error_type: str
    error_message: str
    timestamp: str
    context: Dict[str, Any] = field(default_factory=dict)
    resolution: Optional[str] = None
    resolved: bool = False


class CausalMemory:
    """
    Stores cause-and-effect relationships for self-healing.
    When an error occurs, the system can look up known fixes.
    """
    def __init__(self):
        self.memory_file = MEMORY_DIR / "causal_memory.json"
        self.memories: Dict[str, List[Dict]] = {}
        self._load()
    
    def _load(self):
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    self.memories = json.load(f)
            except:
                self.memories = {}
    
    def _save(self):
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.memories, f, indent=2)
    
    def record_failure(self, component: str, error_type: str, error_msg: str, context: Dict = None):
        """Record a failure occurrence"""
        key = f"{component}:{error_type}"
        if key not in self.memories:
            self.memories[key] = []
        
        self.memories[key].append({
            "timestamp": datetime.now().isoformat(),
            "message": error_msg,
            "context": context or {},
            "resolution": None
        })
        self._save()
    
    def record_resolution(self, component: str, error_type: str, resolution: str):
        """Record how a failure was resolved"""
        key = f"{component}:{error_type}"
        if key in self.memories and self.memories[key]:
            self.memories[key][-1]["resolution"] = resolution
            self._save()
    
    def get_known_fix(self, component: str, error_type: str) -> Optional[str]:
        """Look up a known fix for an error pattern"""
        key = f"{component}:{error_type}"
        if key in self.memories:
            # Find most recent successful resolution
            for record in reversed(self.memories[key]):
                if record.get("resolution"):
                    return record["resolution"]
        return None
    
    def get_failure_count(self, component: str, error_type: str, hours: int = 24) -> int:
        """Count failures in the last N hours"""
        key = f"{component}:{error_type}"
        if key not in self.memories:
            return 0
        
        cutoff = datetime.now() - timedelta(hours=hours)
        count = 0
        for record in self.memories[key]:
            try:
                record_time = datetime.fromisoformat(record["timestamp"])
                if record_time > cutoff:
                    count += 1
            except:
                pass
        return count


class CircuitBreaker:
    """
    Prevents cascading failures by stopping calls to failing services.
    States: CLOSED (normal) -> OPEN (failing) -> HALF_OPEN (testing) -> CLOSED
    """
    def __init__(self, name: str, failure_threshold: int = 3, recovery_timeout: int = 30):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout  # seconds
        
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time: Optional[float] = None
        self.success_count = 0
    
    def can_execute(self) -> bool:
        """Check if execution is allowed"""
        if self.state == CircuitState.CLOSED:
            return True
        
        if self.state == CircuitState.OPEN:
            # Check if recovery timeout has passed
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
                return True
            return False
        
        if self.state == CircuitState.HALF_OPEN:
            return True  # Allow test call
        
        return False
    
    def record_success(self):
        """Record a successful call"""
        self.failure_count = 0
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= 2:  # 2 successes to close
                self.state = CircuitState.CLOSED
                self.success_count = 0
    
    def record_failure(self):
        """Record a failed call"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        self.success_count = 0
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN


class SelfHealingController:
    """
    The main self-healing orchestrator.
    Features:
    - Automatic retry with exponential backoff
    - Circuit breaker per component
    - Causal memory for learning from failures
    - Auto-restart for crashed agents
    """
    def __init__(self):
        self.causal_memory = CausalMemory()
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.agent_health: Dict[str, Dict] = {}
        self.restart_counts: Dict[str, int] = {}
        
    def get_circuit_breaker(self, component: str) -> CircuitBreaker:
        """Get or create a circuit breaker for a component"""
        if component not in self.circuit_breakers:
            self.circuit_breakers[component] = CircuitBreaker(component)
        return self.circuit_breakers[component]
    
    def execute_with_resilience(
        self,
        component: str,
        func: Callable,
        *args,
        max_retries: int = 3,
        base_delay: float = 1.0,
        **kwargs
    ) -> Any:
        """
        Execute a function with full resilience patterns:
        - Circuit breaker check
        - Exponential backoff retries
        - Failure recording
        """
        cb = self.get_circuit_breaker(component)
        
        if not cb.can_execute():
            raise Exception(f"Circuit breaker OPEN for {component}")
        
        last_error = None
        
        for attempt in range(max_retries):
            try:
                result = func(*args, **kwargs)
                cb.record_success()
                return result
                
            except Exception as e:
                last_error = e
                error_type = type(e).__name__
                
                # Record failure
                self.causal_memory.record_failure(
                    component, error_type, str(e),
                    {"attempt": attempt + 1, "args": str(args)[:100]}
                )
                cb.record_failure()
                
                # Check for known fix
                known_fix = self.causal_memory.get_known_fix(component, error_type)
                if known_fix:
                    print(f"[HEALER] Known fix for {error_type}: {known_fix}")
                
                # Exponential backoff
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    print(f"[HEALER] Retry {attempt + 2}/{max_retries} in {delay:.1f}s...")
                    time.sleep(delay)
        
        raise last_error
    
    def resilient(self, component: str, max_retries: int = 3):
        """Decorator for resilient function execution"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return self.execute_with_resilience(
                    component, func, *args, max_retries=max_retries, **kwargs
                )
            return wrapper
        return decorator
    
    def restart_agent(self, agent_name: str, agent_path: Path) -> bool:
        """Attempt to restart a crashed agent"""
        max_restarts = 3
        
        self.restart_counts.setdefault(agent_name, 0)
        
        if self.restart_counts[agent_name] >= max_restarts:
            print(f"[HEALER] Agent {agent_name} exceeded max restarts ({max_restarts})")
            return False
        
        try:
            print(f"[HEALER] Restarting {agent_name}...")
            subprocess.Popen(
                [sys.executable, str(agent_path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            self.restart_counts[agent_name] += 1
            self.causal_memory.record_resolution(agent_name, "CrashError", "auto_restart")
            return True
        except Exception as e:
            print(f"[HEALER] Failed to restart {agent_name}: {e}")
            return False
    
    def get_health_report(self) -> Dict:
        """Get overall system health"""
        return {
            "circuit_breakers": {
                name: {
                    "state": cb.state.value,
                    "failure_count": cb.failure_count
                }
                for name, cb in self.circuit_breakers.items()
            },
            "restart_counts": self.restart_counts,
            "memory_entries": len(self.causal_memory.memories),
            "timestamp": datetime.now().isoformat()
        }


# Singleton
_controller = None

def get_healer() -> SelfHealingController:
    """Get the global self-healing controller"""
    global _controller
    if _controller is None:
        _controller = SelfHealingController()
    return _controller


if __name__ == "__main__":
    # Demo
    healer = get_healer()
    
    @healer.resilient("demo_component", max_retries=2)
    def flaky_function():
        import random
        if random.random() < 0.7:
            raise ValueError("Random failure!")
        return "Success!"
    
    for i in range(5):
        try:
            result = flaky_function()
            print(f"Attempt {i+1}: {result}")
        except Exception as e:
            print(f"Attempt {i+1}: Failed - {e}")
    
    print(f"\nHealth Report: {json.dumps(healer.get_health_report(), indent=2)}")
