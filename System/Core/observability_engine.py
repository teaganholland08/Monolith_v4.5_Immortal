"""
OBSERVABILITY ENGINE - Best-in-World 2026 Standard
Implements: OpenTelemetry-style tracing, Structured Logging, Metrics Collection
Purpose: Full visibility into agent decision-making, latency, and errors.
"""

import json
import time
import functools
import logging
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional
from collections import defaultdict

# --- Configuration ---
LOG_DIR = Path(__file__).parent.parent / "Logs"
LOG_DIR.mkdir(exist_ok=True)

# --- Data Structures ---
@dataclass
class Span:
    """A single unit of traced work (like OpenTelemetry Span)"""
    trace_id: str
    span_id: str
    name: str
    start_time: float
    end_time: Optional[float] = None
    status: str = "RUNNING"
    attributes: Dict[str, Any] = field(default_factory=dict)
    events: List[Dict] = field(default_factory=list)
    parent_span_id: Optional[str] = None
    
    def add_event(self, name: str, attributes: Optional[Dict] = None):
        self.events.append({
            "name": name,
            "timestamp": time.time(),
            "attributes": attributes or {}
        })
    
    def set_status(self, status: str, message: str = ""):
        self.status = status
        if message:
            self.attributes["status_message"] = message
            
    def finish(self, status: str = "OK"):
        self.end_time = time.time()
        self.status = status


class ObservabilityEngine:
    """
    Central Observability Hub for Project Monolith.
    Features:
    - Distributed Tracing (Span-based)
    - Structured Logging (JSON Lines)
    - Metrics Collection (Counters, Latencies)
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.traces: Dict[str, List[Span]] = defaultdict(list)
        self.metrics: Dict[str, float] = defaultdict(float)
        self.counters: Dict[str, int] = defaultdict(int)
        self.log_file = LOG_DIR / "observability.jsonl"
        
        # Configure structured logging
        self.logger = logging.getLogger("monolith.observability")
        self.logger.setLevel(logging.DEBUG)
        
        handler = logging.FileHandler(self.log_file, encoding='utf-8')
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)
        
        self._initialized = True
        self._log_event("INIT", {"message": "Observability Engine Started"})
    
    def _generate_id(self) -> str:
        import random
        return f"{int(time.time()*1000)}-{random.randint(1000, 9999)}"
    
    def _log_event(self, event_type: str, data: Dict):
        """Write structured JSON log line"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            **data
        }
        self.logger.info(json.dumps(entry))
    
    # --- Tracing API ---
    def start_trace(self, name: str) -> str:
        """Start a new trace, returns trace_id"""
        trace_id = self._generate_id()
        span = Span(
            trace_id=trace_id,
            span_id=self._generate_id(),
            name=name,
            start_time=time.time()
        )
        self.traces[trace_id].append(span)
        self._log_event("TRACE_START", {"trace_id": trace_id, "name": name})
        return trace_id
    
    def start_span(self, trace_id: str, name: str, parent_span_id: Optional[str] = None) -> Span:
        """Start a child span within a trace"""
        span = Span(
            trace_id=trace_id,
            span_id=self._generate_id(),
            name=name,
            start_time=time.time(),
            parent_span_id=parent_span_id
        )
        self.traces[trace_id].append(span)
        return span
    
    def end_span(self, span: Span, status: str = "OK"):
        """End a span"""
        span.finish(status)
        latency = span.end_time - span.start_time
        self.record_latency(f"span.{span.name}", latency)
        self._log_event("SPAN_END", {
            "trace_id": span.trace_id,
            "span_id": span.span_id,
            "name": span.name,
            "status": status,
            "latency_ms": latency * 1000
        })
    
    def end_trace(self, trace_id: str, status: str = "OK"):
        """End an entire trace"""
        spans = self.traces.get(trace_id, [])
        if spans:
            root_span = spans[0]
            root_span.finish(status)
            total_latency = root_span.end_time - root_span.start_time
            self._log_event("TRACE_END", {
                "trace_id": trace_id,
                "name": root_span.name,
                "status": status,
                "total_latency_ms": total_latency * 1000,
                "span_count": len(spans)
            })
    
    # --- Metrics API ---
    def increment(self, metric_name: str, value: int = 1):
        """Increment a counter"""
        self.counters[metric_name] += value
    
    def record_latency(self, metric_name: str, latency_seconds: float):
        """Record a latency measurement"""
        self.metrics[f"{metric_name}.last"] = latency_seconds
        # Running average (simplified)
        key = f"{metric_name}.avg"
        if key in self.metrics:
            self.metrics[key] = (self.metrics[key] + latency_seconds) / 2
        else:
            self.metrics[key] = latency_seconds
    
    def get_metrics_snapshot(self) -> Dict:
        """Get current metrics state"""
        return {
            "counters": dict(self.counters),
            "latencies": dict(self.metrics),
            "active_traces": len(self.traces),
            "snapshot_time": datetime.now().isoformat()
        }
    
    # --- Decorator for Easy Instrumentation ---
    def trace(self, name: Optional[str] = None):
        """Decorator to automatically trace a function"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                span_name = name or func.__name__
                trace_id = self.start_trace(span_name)
                root_span = self.traces[trace_id][0]
                
                try:
                    result = func(*args, **kwargs)
                    self.end_span(root_span, "OK")
                    self.end_trace(trace_id, "OK")
                    return result
                except Exception as e:
                    root_span.add_event("exception", {"type": type(e).__name__, "message": str(e)})
                    self.end_span(root_span, "ERROR")
                    self.end_trace(trace_id, "ERROR")
                    self.increment("errors.total")
                    raise
            return wrapper
        return decorator


# Singleton instance
obs = ObservabilityEngine()


def get_observability() -> ObservabilityEngine:
    """Get the global observability engine instance"""
    return obs


if __name__ == "__main__":
    # Demo
    engine = get_observability()
    
    @engine.trace("demo_operation")
    def demo():
        time.sleep(0.1)
        print("Demo operation executed")
        return "OK"
    
    demo()
    print(f"Metrics: {engine.get_metrics_snapshot()}")
