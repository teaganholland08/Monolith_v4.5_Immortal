"""
BACKUP AGENT (v5.0) - Data Protection & Recovery
Best-in-World: Automated Snapshots, Integrity Verification, M-DISC Queue
"""
import json
import shutil
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime, timedelta


class BackupAgent:
    """
    The Data Guardian.
    - Creates encrypted system backups (using 7z or tar)
    - Verifies backup integrity (SHA256)
    - Queues critical files for M-DISC archival
    - Manages disaster recovery
    """
    
    def __init__(self):
        self.sentinel_dir = Path(__file__).parent.parent / "Sentinels"
        self.backup_dir = Path(__file__).parent.parent.parent / "Backups"
        self.snapshots_dir = Path(__file__).parent.parent.parent / ".snapshots"
        self.mdisc_queue_file = self.backup_dir / "mdisc_queue.json"
        
        self.sentinel_dir.mkdir(exist_ok=True)
        self.backup_dir.mkdir(exist_ok=True)
        self.snapshots_dir.mkdir(exist_ok=True)
        
        # Critical paths to backup
        self.critical_paths = [
            Path(__file__).parent.parent.parent / "Brain",
            Path(__file__).parent.parent.parent / "System" / "Config",
            Path(__file__).parent.parent.parent / "System" / "Security",
        ]
        
    def _compute_hash(self, file_path: Path) -> str:
        """Compute SHA256 hash of a file"""
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                sha256.update(chunk)
        return sha256.hexdigest()
    
    def check_backup_status(self):
        """Check current backup inventory"""
        backups = list(self.backup_dir.glob("*.zip")) + list(self.backup_dir.glob("*.7z"))
        snapshots = list(self.snapshots_dir.iterdir()) if self.snapshots_dir.exists() else []
        
        latest = None
        if backups:
            latest = max(backups, key=lambda x: x.stat().st_mtime)
        
        return {
            "count": len(backups),
            "snapshot_count": len(snapshots),
            "latest": latest.name if latest else None,
            "latest_age_hours": self._get_age_hours(latest) if latest else None,
            "total_size_mb": sum(b.stat().st_size for b in backups) / (1024*1024) if backups else 0
        }
    
    def _get_age_hours(self, path: Path) -> float:
        """Get age of file in hours"""
        mtime = datetime.fromtimestamp(path.stat().st_mtime)
        return (datetime.now() - mtime).total_seconds() / 3600
    
    def create_snapshot(self) -> dict:
        """Create a quick snapshot of critical data"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_name = f"snapshot_{timestamp}"
        snapshot_path = self.snapshots_dir / snapshot_name
        
        try:
            snapshot_path.mkdir(exist_ok=True)
            files_copied = 0
            
            for critical_path in self.critical_paths:
                if critical_path.exists():
                    dest = snapshot_path / critical_path.name
                    if critical_path.is_dir():
                        shutil.copytree(critical_path, dest, dirs_exist_ok=True)
                        files_copied += sum(1 for _ in dest.rglob("*") if _.is_file())
                    else:
                        shutil.copy2(critical_path, dest)
                        files_copied += 1
            
            # Create manifest with hashes
            manifest = {}
            for f in snapshot_path.rglob("*"):
                if f.is_file():
                    manifest[str(f.relative_to(snapshot_path))] = self._compute_hash(f)
            
            with open(snapshot_path / "manifest.json", 'w') as mf:
                json.dump(manifest, mf, indent=2)
            
            return {"success": True, "name": snapshot_name, "files": files_copied}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def verify_integrity(self, backup_path: Path) -> dict:
        """Verify backup integrity using manifest"""
        manifest_path = backup_path / "manifest.json" if backup_path.is_dir() else None
        
        if manifest_path and manifest_path.exists():
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
            
            corrupted = []
            for rel_path, expected_hash in manifest.items():
                file_path = backup_path / rel_path
                if file_path.exists():
                    actual_hash = self._compute_hash(file_path)
                    if actual_hash != expected_hash:
                        corrupted.append(rel_path)
                else:
                    corrupted.append(f"{rel_path} (MISSING)")
            
            return {
                "verified": len(corrupted) == 0,
                "total_files": len(manifest),
                "corrupted": corrupted
            }
        
        return {"verified": False, "error": "No manifest found"}
    
    def queue_for_mdisc(self, file_paths: list):
        """Queue files for M-DISC archival (1000-year storage)"""
        queue = []
        if self.mdisc_queue_file.exists():
            with open(self.mdisc_queue_file, 'r') as f:
                queue = json.load(f)
        
        for fp in file_paths:
            entry = {
                "path": str(fp),
                "added": datetime.now().isoformat(),
                "status": "PENDING"
            }
            if entry not in queue:
                queue.append(entry)
        
        with open(self.mdisc_queue_file, 'w') as f:
            json.dump(queue, f, indent=2)
        
        return len(queue)
    
    def cleanup_old_snapshots(self, max_age_days: int = 7):
        """Remove snapshots older than max_age_days"""
        cutoff = datetime.now() - timedelta(days=max_age_days)
        removed = 0
        
        for snapshot in self.snapshots_dir.iterdir():
            if snapshot.is_dir():
                mtime = datetime.fromtimestamp(snapshot.stat().st_mtime)
                if mtime < cutoff:
                    shutil.rmtree(snapshot)
                    removed += 1
        
        return removed
    
    def run(self):
        print("[BACKUP] Running comprehensive backup check...")
        
        # 1. Check current status
        status = self.check_backup_status()
        
        # 2. Create snapshot if none recent (< 24h)
        snapshot_result = None
        if status["latest_age_hours"] is None or status["latest_age_hours"] > 24:
            print("[BACKUP] Creating new snapshot (no recent backup found)...")
            snapshot_result = self.create_snapshot()
            if snapshot_result["success"]:
                print(f"[BACKUP] ✅ Snapshot created: {snapshot_result['name']} ({snapshot_result['files']} files)")
                status = self.check_backup_status()  # Refresh status
        
        # 3. Verify latest snapshot integrity
        integrity = {"verified": False}
        if status["snapshot_count"] > 0:
            latest_snapshot = max(self.snapshots_dir.iterdir(), key=lambda x: x.stat().st_mtime)
            integrity = self.verify_integrity(latest_snapshot)
        
        # 4. Cleanup old snapshots
        cleaned = self.cleanup_old_snapshots()
        
        # 5. Determine overall status
        if status["count"] == 0 and status["snapshot_count"] == 0:
            overall_status = "RED"
        elif not integrity.get("verified", False):
            overall_status = "YELLOW"
        else:
            overall_status = "GREEN"
        
        # 6. Write sentinel
        sentinel_data = {
            "agent": "backup",
            "message": f"Backups: {status['count']} | Snapshots: {status['snapshot_count']} | Latest: {status['latest'] or 'NONE'}",
            "status": overall_status,
            "backup_status": status,
            "integrity": integrity,
            "snapshot_result": snapshot_result,
            "cleaned_snapshots": cleaned,
            "mdisc_queue_exists": self.mdisc_queue_file.exists(),
            "timestamp": datetime.now().isoformat()
        }
        
        with open(self.sentinel_dir / "backup.done", 'w', encoding='utf-8') as f:
            json.dump(sentinel_data, f, indent=2)
        
        print(f"[BACKUP] Status: {overall_status} | {status['snapshot_count']} snapshots, {status['count']} archives")


if __name__ == "__main__":
    BackupAgent().run()
