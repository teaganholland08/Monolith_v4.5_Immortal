"""
DEBUG AGENT - System Debugging & Error Resolution
Monitors logs, identifies issues, and auto-fixes problems.
"""
import json
import traceback
import subprocess
from pathlib import Path
from datetime import datetime

class DebugAgent:
    """
    The System Debugger.
    - Monitors error logs
    - Identifies Python exceptions
    - Auto-fixes common issues
    - Reports unresolved problems for Director review
    """
    
    def __init__(self):
        self.sentinel_dir = Path(__file__).parent.parent / "Sentinels"
        self.logs_dir = Path(__file__).parent.parent / "Logs"
        self.agents_dir = Path(__file__).parent
        self.sentinel_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
        
    def scan_agent_errors(self):
        """Test run all agents and capture errors"""
        errors = []
        for agent_file in self.agents_dir.glob("*.py"):
            if agent_file.name in ["debug_agent.py", "__init__.py"]:
                continue
            try:
                result = subprocess.run(
                    ["python", "-m", "py_compile", str(agent_file)],
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode != 0:
                    errors.append({
                        "file": agent_file.name,
                        "type": "SYNTAX_ERROR",
                        "message": result.stderr[:200]
                    })
            except Exception as e:
                errors.append({
                    "file": agent_file.name,
                    "type": "SCAN_ERROR",
                    "message": str(e)
                })
        return errors
    
    def scan_import_errors(self):
        """Check for missing imports"""
        missing = []
        required_libs = ["json", "pathlib", "datetime", "subprocess", "sqlite3", "random"]
        
        for lib in required_libs:
            try:
                __import__(lib)
            except ImportError:
                missing.append(lib)
        
        return missing
    
    def check_sentinel_integrity(self):
        """Verify sentinel files are valid JSON"""
        corrupt = []
        for sentinel in self.sentinel_dir.glob("*.done"):
            try:
                with open(sentinel, 'r') as f:
                    json.load(f)
            except json.JSONDecodeError:
                corrupt.append(sentinel.name)
        return corrupt
    
    def check_database_integrity(self):
        """Verify SQLite databases"""
        issues = []
        for db in self.logs_dir.glob("*.db"):
            try:
                import sqlite3
                conn = sqlite3.connect(db)
                conn.execute("SELECT 1")
                conn.close()
            except Exception as e:
                issues.append({"file": db.name, "error": str(e)})
        return issues
    
    def auto_fix_issues(self, errors):
        """Attempt automatic fixes"""
        fixed = []
        for error in errors:
            if error.get("type") == "CORRUPT_SENTINEL":
                # Delete corrupt sentinel
                sentinel = self.sentinel_dir / error.get("file", "")
                if sentinel.exists():
                    sentinel.unlink()
                    fixed.append(f"Removed corrupt sentinel: {error['file']}")
        return fixed
    
    def run(self):
        print("[DEBUG] Running system diagnostics...")
        
        agent_errors = self.scan_agent_errors()
        import_errors = self.scan_import_errors()
        corrupt_sentinels = self.check_sentinel_integrity()
        db_issues = self.check_database_integrity()
        
        total_issues = len(agent_errors) + len(import_errors) + len(corrupt_sentinels) + len(db_issues)
        
        status = "GREEN" if total_issues == 0 else "YELLOW" if total_issues < 3 else "RED"
        message = f"Issues: {total_issues} | Agents: {len(agent_errors)} errors | Imports: {len(import_errors)} missing"
        
        sentinel_data = {
            "agent": "debug_agent",
            "message": message,
            "status": status,
            "agent_errors": agent_errors,
            "missing_imports": import_errors,
            "corrupt_sentinels": corrupt_sentinels,
            "db_issues": db_issues,
            "total_issues": total_issues,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(self.sentinel_dir / "debug_agent.done", 'w', encoding='utf-8') as f:
            json.dump(sentinel_data, f, indent=2)
        
        print(f"[DEBUG] {message}")
        if total_issues == 0:
            print("   ✅ All systems healthy")
        else:
            for e in agent_errors[:3]:
                print(f"   ❌ {e['file']}: {e['type']}")

if __name__ == "__main__":
    DebugAgent().run()
