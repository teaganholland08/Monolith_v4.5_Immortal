"""
SYSTEM HYGIENE AGENT - Project Monolith v5.5
Purpose: Maintain system health, disk longevity, and log rotation for "Immortal" status.
Optimized for: i3/4GB low-spec hardware.
"""

import os
import shutil
import time
import json
from pathlib import Path
from datetime import datetime, timedelta

class SystemHygiene:
    def __init__(self):
        self.root = Path(__file__).parent.parent.parent
        self.logs_dir = self.root / "Logs"
        self.sentinel_dir = self.root / "System" / "Sentinels"
        self.backups_dir = self.root / "Backups" / "Logs"
        
        # Thresholds
        self.max_log_size_mb = 10
        self.retention_days_sentinels = 2
        self.min_disk_space_gb = 2

        # Ensure directories
        self.backups_dir.mkdir(parents=True, exist_ok=True)

    def rotate_logs(self):
        """Rotate and compress logs bigger than threshold"""
        print("[HYGIENE] Rotating logs...")
        for log_file in self.logs_dir.rglob("*.log*"):
            if log_file.is_file() and log_file.stat().st_size > self.max_log_size_mb * 1024 * 1024:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                archive_name = self.backups_dir / f"{log_file.stem}_{timestamp}.log.bak"
                print(f"[HYGIENE] Archiving {log_file.name} to {archive_name.name}")
                shutil.move(str(log_file), str(archive_name))
                # Create a new empty log file
                log_file.touch()

    def clean_sentinels(self):
        """Remove old .done files to keep system clean"""
        print("[HYGIENE] Cleaning old sentinels...")
        cutoff = datetime.now() - timedelta(days=self.retention_days_sentinels)
        for sentinel in self.sentinel_dir.glob("*.done"):
            if sentinel.is_file():
                mtime = datetime.fromtimestamp(sentinel.stat().st_mtime)
                if mtime < cutoff:
                    print(f"[HYGIENE] Removing expired sentinel: {sentinel.name}")
                    sentinel.unlink()

    def check_disk_space(self):
        """Monitor disk space and alert if critical"""
        usage = shutil.disk_usage(self.root)
        free_gb = usage.free / (1024**3)
        print(f"[HYGIENE] Free disk space: {free_gb:.2f} GB")
        
        status = "GREEN"
        if free_gb < self.min_disk_space_gb:
            status = "RED"
            print(f"[HYGIENE] ALERT: CRITICAL DISK SPACE! ({free_gb:.2f} GB)")
        elif free_gb < self.min_disk_space_gb * 2:
            status = "YELLOW"
            print(f"[HYGIENE] Warning: Low disk space. ({free_gb:.2f} GB)")
            
        return status, free_gb

    def run(self):
        print(f"[HYGIENE] Starting Cycle: {datetime.now().isoformat()}")
        
        self.rotate_logs()
        self.clean_sentinels()
        status, free_gb = self.check_disk_space()
        
        report = {
            "agent": "system_hygiene",
            "status": status,
            "message": f"Hygiene cycle complete. Free space: {free_gb:.2f} GB",
            "timestamp": datetime.now().isoformat(),
            "details": {
                "free_gb": free_gb,
                "logs_rotated": True,
                "sentinels_cleaned": True
            }
        }
        
        with open(self.sentinel_dir / "system_hygiene.done", 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
            
        print("[HYGIENE] Cycle Complete.")

if __name__ == "__main__":
    SystemHygiene().run()
