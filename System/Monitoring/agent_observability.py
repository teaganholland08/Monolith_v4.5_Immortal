"""
AGENT OBSERVABILITY SYSTEM
2026 best practices for autonomous agent monitoring

Features:
- Performance tracking (execution time, success rate)
- Error logging and debugging
- Agent health monitoring
- Execution tracing
- Cost tracking (API calls, compute)
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime, timedelta
import time

class AgentObservability:
    """
    Comprehensive observability for autonomous agents
    
    Tracks:
    - Execution metrics (time, status, errors)
    - Performance trends (success rate, avg duration)
    - Resource usage (API calls, compute time)
    - Agent health (last run, error rate)
    """
    
    def __init__(self):
        self.db_path = Path(__file__).parent.parent / "Logs" / "ledger.db"
        self.logs_dir = Path(__file__).parent.parent / "Logs" / "agent_traces"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        self._init_observability_tables()
    
    def _init_observability_tables(self):
        """Create observability tracking tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Agent execution log
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_executions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_name TEXT NOT NULL,
                started_at TEXT NOT NULL,
                completed_at TEXT,
                duration_ms INTEGER,
                status TEXT,
                error_message TEXT,
                output TEXT,
                api_calls_made INTEGER DEFAULT 0,
                tokens_used INTEGER DEFAULT 0
            )
        """)
        
        # Agent performance metrics
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_metrics (
                agent_name TEXT PRIMARY KEY,
                total_runs INTEGER DEFAULT 0,
                successful_runs INTEGER DEFAULT 0,
                failed_runs INTEGER DEFAULT 0,
                avg_duration_ms REAL DEFAULT 0,
                last_run TEXT,
                last_success TEXT,
                last_error TEXT,
                error_rate REAL DEFAULT 0
            )
        """)
        
        conn.commit()
        conn.close()
    
    def start_execution(self, agent_name):
        """
        Log agent execution start
        
        Returns: execution_id for tracking
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO agent_executions (agent_name, started_at, status)
            VALUES (?, ?, 'RUNNING')
        """, (agent_name, datetime.now().isoformat()))
        
        execution_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        return execution_id
    
    def complete_execution(self, execution_id, status, output=None, error_message=None, 
                          api_calls=0, tokens_used=0):
        """Log agent execution completion"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get start time
        cursor.execute("""
            SELECT started_at, agent_name FROM agent_executions WHERE id = ?
        """, (execution_id,))
        
        result = cursor.fetchone()
        if not result:
            conn.close()
            return
        
        started_at, agent_name = result
        started_time = datetime.fromisoformat(started_at)
        duration_ms = int((datetime.now() - started_time).total_seconds() * 1000)
        
        # Update execution record
        cursor.execute("""
            UPDATE agent_executions
            SET completed_at = ?,
                duration_ms = ?,
                status = ?,
                error_message = ?,
                output = ?,
                api_calls_made = ?,
                tokens_used = ?
            WHERE id = ?
        """, (datetime.now().isoformat(), duration_ms, status, error_message, 
              output, api_calls, tokens_used, execution_id))
        
        # Update agent metrics
        self._update_agent_metrics(cursor, agent_name, status, duration_ms, error_message)
        
        conn.commit()
        conn.close()
    
    def _update_agent_metrics(self, cursor, agent_name, status, duration_ms, error_message):
        """Update aggregate metrics for agent"""
        
        # Get current metrics
        cursor.execute("""
            SELECT total_runs, successful_runs, failed_runs, avg_duration_ms
            FROM agent_metrics WHERE agent_name = ?
        """, (agent_name,))
        
        result = cursor.fetchone()
        
        if result:
            total_runs, successful_runs, failed_runs, avg_duration = result
        else:
            total_runs = successful_runs = failed_runs = 0
            avg_duration = 0
        
        # Update counts
        total_runs += 1
        if status == "SUCCESS":
            successful_runs += 1
        elif status == "FAILED":
            failed_runs += 1
        
        # Update average duration
        avg_duration = ((avg_duration * (total_runs - 1)) + duration_ms) / total_runs
        
        # Calculate error rate
        error_rate = (failed_runs / total_runs) * 100 if total_runs > 0 else 0
        
        # Upsert metrics
        cursor.execute("""
            INSERT OR REPLACE INTO agent_metrics
            (agent_name, total_runs, successful_runs, failed_runs, avg_duration_ms,
             last_run, last_success, last_error, error_rate)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            agent_name,
            total_runs,
            successful_runs,
            failed_runs,
            avg_duration,
            datetime.now().isoformat(),
            datetime.now().isoformat() if status == "SUCCESS" else None,
            error_message if status == "FAILED" else None,
            error_rate
        ))
    
    def get_agent_health(self, agent_name):
        """Get health status for an agent"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT total_runs, successful_runs, failed_runs, avg_duration_ms,
                   last_run, error_rate
            FROM agent_metrics WHERE agent_name = ?
        """, (agent_name,))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return {"status": "UNKNOWN", "message": "No execution history"}
        
        total_runs, successful_runs, failed_runs, avg_duration, last_run, error_rate = result
        
        # Determine health status
        if error_rate > 50:
            status = "CRITICAL"
        elif error_rate > 20:
            status = "DEGRADED"
        elif total_runs == 0:
            status = "UNKNOWN"
        else:
            status = "HEALTHY"
        
        # Check staleness
        if last_run:
            last_run_time = datetime.fromisoformat(last_run)
            hours_since = (datetime.now() - last_run_time).total_seconds() / 3600
            
            if hours_since > 48:
                status = "STALE"
        
        return {
            "agent": agent_name,
            "status": status,
            "total_runs": total_runs,
            "success_rate": round((successful_runs / total_runs) * 100, 1) if total_runs > 0 else 0,
            "error_rate": round(error_rate, 1),
            "avg_duration_ms": round(avg_duration, 1),
            "last_run": last_run
        }
    
    def get_recent_errors(self, hours=24, limit=10):
        """Get recent agent errors for debugging"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff = (datetime.now() - timedelta(hours=hours)).isoformat()
        
        cursor.execute("""
            SELECT agent_name, started_at, error_message, output
            FROM agent_executions
            WHERE status = 'FAILED' AND started_at > ?
            ORDER BY started_at DESC
            LIMIT ?
        """, (cutoff, limit))
        
        errors = []
        for row in cursor.fetchall():
            errors.append({
                "agent": row[0],
                "timestamp": row[1],
                "error": row[2],
                "output": row[3]
            })
        
        conn.close()
        return errors
    
    def generate_health_report(self):
        """Generate comprehensive health report for all agents"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT agent_name FROM agent_metrics
            ORDER BY error_rate DESC
        """)
        
        agents = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        print("\n" + "="*60)
        print("AGENT HEALTH REPORT")
        print("="*60)
        
        for agent_name in agents:
            health = self.get_agent_health(agent_name)
            
            status_icon = {
                "HEALTHY": "[OK]",
                "DEGRADED": "[WARN]",
                "CRITICAL": "[CRIT]",
                "STALE": "[STALE]",
                "UNKNOWN": "[?]"
            }.get(health["status"], "[?]")
            
            print(f"\n{status_icon} {agent_name}")
            print(f"   Status: {health['status']}")
            print(f"   Success Rate: {health['success_rate']}%")
            print(f"   Error Rate: {health['error_rate']}%")
            print(f"   Avg Duration: {health['avg_duration_ms']}ms")
            print(f"   Last Run: {health['last_run']}")
        
        print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    obs = AgentObservability()
    obs.generate_health_report()
