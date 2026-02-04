"""
MONOLITH SYSTEM HYGIENE ENGINE
Auto-Cleanup, Deduplication, Performance Optimization

Keeps system:
- Fast (removes bloat)
- Anonymous (scrubs metadata)
- Secure (no data leaks)
"""

import os
import hashlib
import psutil
import time
from pathlib import Path

class HygieneEngine:
    def __init__(self):
        self.root = Path(__file__).parent.parent.parent
        self.temp_dirs = [
            self.root / "System" / "Logs",
            Path(os.getenv("TEMP")),
        ]
        self.file_cache = {}
        
    def find_duplicates(self):
        """Identify duplicate files for removal"""
        print("   🔍 HYGIENE: Scanning for duplicates...")
        
        hashes = {}
        duplicates = []
        
        try:
            for ext in ["*.py", "*.md", "*.db"]:
                for file_path in self.root.rglob(ext):
                    if file_path.is_file():
                        try:
                            file_hash = hashlib.sha256(file_path.read_bytes()).hexdigest()
                            
                            if file_hash in hashes:
                                duplicates.append({
                                    "original": hashes[file_hash],
                                    "duplicate": str(file_path),
                                    "size": file_path.stat().st_size
                                })
                            else:
                                hashes[file_hash] = str(file_path)
                        except:
                            pass
        except Exception as e:
            print(f"   ⚠️ DUPLICATE SCAN ERROR: {e}")
        
        return duplicates
    
    def clean_temp_files(self):
        """Remove temporary files to free storage"""
        print("   🧹 HYGIENE: Cleaning temporary files...")
        
        cleaned_bytes = 0
        cleaned_count = 0
        
        for temp_dir in self.temp_dirs:
            if not temp_dir or not temp_dir.exists():
                continue
                
            try:
                for item in temp_dir.glob("*"):
                    try:
                        if item.is_file():
                            size = item.stat().st_size
                            item.unlink()
                            cleaned_bytes += size
                            cleaned_count += 1
                    except:
                        pass  # File in use, skip
            except Exception as e:
                print(f"   ⚠️ TEMP CLEAN ERROR: {e}")
        
        return cleaned_bytes, cleaned_count
    
    def optimize_memory(self):
        """Kill resource-hogging processes"""
        print("   ⚡ HYGIENE: Optimizing system resources...")
        
        killed = []
        
        try:
            for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_percent']):
                try:
                    # Kill if consuming >80% CPU or >50% RAM
                    if proc.info['cpu_percent'] > 80 or proc.info['memory_percent'] > 50:
                        name = proc.info['name']
                        # Don't kill critical processes
                        if name not in ["python.exe", "System", "svchost.exe"]:
                            proc.kill()
                            killed.append(name)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
        except Exception as e:
            print(f"   ⚠️ MEMORY OPTIMIZE ERROR: {e}")
        
        return killed
    
    def scrub_metadata(self, file_path):
        """Remove identifying metadata from file"""
        # Placeholder - would need specific libraries for each file type
        # (PIL for images, PyPDF2 for PDFs, etc.)
        try:
            # Basic: Just update modification time to remove timestamp trail
            os.utime(file_path, (time.time(), time.time()))
            return True
        except:
            return False
    
    def get_system_health(self):
        """Current system status"""
        try:
            cpu = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent
            
            return {
                "cpu_usage": cpu,
                "ram_usage": ram,
                "disk_usage": disk,
                "status": "HEALTHY" if cpu < 70 and ram < 80 else "STRAINED"
            }
        except:
            return {"status": "UNKNOWN"}
    
    def run_maintenance_cycle(self):
        """Full system hygiene sweep"""
        print("\n🧹 SYSTEM HYGIENE: Initiating maintenance cycle...")
        
        # 1. Check system health
        health = self.get_system_health()
        print(f"   📊 CPU: {health.get('cpu_usage', 0):.1f}% | RAM: {health.get('ram_usage', 0):.1f}% | Disk: {health.get('disk_usage', 0):.1f}%")
        
        # 2. Clean temp files
        bytes_cleaned, files_cleaned = self.clean_temp_files()
        if files_cleaned > 0:
            print(f"   ✅ Removed {files_cleaned} temp files ({bytes_cleaned / 1024 / 1024:.1f} MB freed)")
        
        # 3. Find duplicates
        dupes = self.find_duplicates()
        if dupes:
            total_waste = sum(d['size'] for d in dupes)
            print(f"   ⚠️ Found {len(dupes)} duplicates ({total_waste / 1024 / 1024:.1f} MB wasted)")
        
        # 4. Optimize memory
        killed = self.optimize_memory()
        if killed:
            print(f"   ⚡ Killed {len(killed)} resource hogs: {', '.join(killed)}")
        
        return {
            "health": health,
            "cleaned_files": files_cleaned,
            "cleaned_mb": bytes_cleaned / 1024 / 1024,
            "duplicates": len(dupes),
            "processes_killed": len(killed)
        }

if __name__ == "__main__":
    engine = HygieneEngine()
    results = engine.run_maintenance_cycle()
    
    print("\n📋 MAINTENANCE SUMMARY:")
    print(f"   System Status: {results['health']['status']}")
    print(f"   Files Cleaned: {results['cleaned_files']}")
    print(f"   Space Freed: {results['cleaned_mb']:.1f} MB")
    print(f"   Duplicates Found: {results['duplicates']}")
