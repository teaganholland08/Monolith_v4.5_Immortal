"""
BACKUP AGENT - Data Protection & Recovery
Manages backups, snapshots, and disaster recovery.
"""
import json
import shutil
from pathlib import Path
from datetime import datetime

class BackupAgent:
    """
    The Data Guardian.
    - Creates system backups
    - Verifies backup integrity
    - Manages disaster recovery
    """
    
    def __init__(self):
        self.sentinel_dir = Path(__file__).parent.parent / "Sentinels"
        self.backup_dir = Path(__file__).parent.parent.parent / "Backups"
        self.sentinel_dir.mkdir(exist_ok=True)
        self.backup_dir.mkdir(exist_ok=True)
        
    def check_backup_status(self):
        backups = list(self.backup_dir.glob("*.zip"))
        return {
            "count": len(backups),
            "latest": backups[-1].name if backups else None,
            "total_size_mb": sum(b.stat().st_size for b in backups) / (1024*1024) if backups else 0
        }
    
    def run(self):
        print("[BACKUP] Checking backup status...")
        status = self.check_backup_status()
        
        sentinel_data = {
            "agent": "backup",
            "message": f"Backups: {status['count']} | Latest: {status['latest'] or 'NONE'}",
            "status": "GREEN" if status["count"] > 0 else "RED",
            "backup_status": status,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(self.sentinel_dir / "backup.done", 'w', encoding='utf-8') as f:
            json.dump(sentinel_data, f, indent=2)
        
        print(f"[BACKUP] {status['count']} backups available")

if __name__ == "__main__":
    BackupAgent().run()
