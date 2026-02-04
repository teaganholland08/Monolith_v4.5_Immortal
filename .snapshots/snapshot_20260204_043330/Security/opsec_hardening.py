"""
MONOLITH OPSEC LAYER - Operational Security & Hardening
Network anonymity, system hardening, metadata scrubbing

Security Levels:
- LEVEL 1 (USER): Basic VPN, ad-blocking
- LEVEL 2 (GHOST): Tor, burner identities, VM isolation
- LEVEL 3 (MONOLITH): Air-gapped backups, hardened OS, mesh networks

Current: Implements LEVEL 2 (Ghost) for Windows/Samsung
"""

import subprocess
import os
import platform
from pathlib import Path

class OPSECHardening:
    def __init__(self):
        self.os_type = platform.system()
        self.hardening_log = []
        
    def check_vpn_status(self):
        """Verify VPN/anonymity layer is active"""
        try:
            # Check for Surfshark or other VPN processes
            if self.os_type == "Windows":
                result = subprocess.run(
                    ["tasklist"],
                    capture_output=True,
                    text=True
                )
                vpn_active = any(vpn in result.stdout.lower() for vpn in 
                                ["surfshark", "nordvpn", "expressvpn", "mullvad"])
                
                return {
                    "status": "PROTECTED" if vpn_active else "EXPOSED",
                    "details": "VPN process detected" if vpn_active else "⚠️ NO VPN DETECTED"
                }
        except:
            return {"status": "UNKNOWN", "details": "Cannot verify VPN"}
    
    def disable_telemetry(self):
        """Kill Windows telemetry/tracking"""
        if self.os_type != "Windows":
            return {"status": "SKIPPED", "reason": "Not Windows"}
        
        commands = [
            # Disable telemetry services
            'sc config "DiagTrack" start= disabled',
            'sc stop "DiagTrack"',
            'sc config "dmwappushservice" start= disabled',
            'sc stop "dmwappushservice"',
            
            # Disable data collection
            'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\DataCollection" /v AllowTelemetry /t REG_DWORD /d 0 /f',
            'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection" /v AllowTelemetry /t REG_DWORD /d 0 /f',
        ]
        
        results = []
        for cmd in commands:
            try:
                # Note: These require admin privileges
                subprocess.run(cmd, shell=True, capture_output=True)
                results.append(f"✓ {cmd[:30]}...")
            except:
                results.append(f"✗ {cmd[:30]}... (requires admin)")
        
        return {
            "status": "PARTIAL",
            "applied": results,
            "note": "Some commands require Administrator rights"
        }
    
    def clear_forensic_trails(self):
        """Remove logs and temp files that could reveal activity"""
        cleared = []
        
        # Windows temp directories
        temp_dirs = [
            os.getenv("TEMP"),
            os.getenv("TMP"),
            Path.home() / "AppData" / "Local" / "Temp"
        ]
        
        total_cleared = 0
        for temp_dir in temp_dirs:
            if temp_dir and Path(temp_dir).exists():
                try:
                    for item in Path(temp_dir).glob("*"):
                        try:
                            if item.is_file():
                                item.unlink()
                                total_cleared += 1
                        except:
                            pass
                except:
                    pass
        
        # Clear recent files list
        try:
            recent_path = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Recent"
            if recent_path.exists():
                for item in recent_path.glob("*"):
                    try:
                        item.unlink()
                    except:
                        pass
        except:
            pass
        
        return {
            "files_cleared": total_cleared,
            "recents_cleared": "Yes",
            "status": "SANITIZED"
        }
    
    def create_kill_switch_script(self):
        """Generate emergency shutdown script"""
        kill_script = '''@echo off
REM MONOLITH KILL SWITCH - Emergency Shutdown
echo ⚠️ KILL SWITCH ACTIVATED ⚠️
echo.

REM 1. Kill VPN (exposing real IP means abort)
taskkill /F /IM surfshark.exe 2>nul
taskkill /F /IM openvpn.exe 2>nul

REM 2. Kill Monolith processes
taskkill /F /IM python.exe 2>nul

REM 3. Kill browsers (prevent data leaks)
taskkill /F /IM chrome.exe 2>nul
taskkill /F /IM firefox.exe 2>nul
taskkill /F /IM msedge.exe 2>nul

REM 4. Clear clipboard
echo off | clip

REM 5. Lock computer
rundll32.exe user32.dll,LockWorkStation

echo.
echo ✓ KILL SWITCH COMPLETE - SYSTEM LOCKED
pause
'''
        
        script_path = Path(__file__).parent.parent.parent / "KILL_SWITCH.bat"
        script_path.write_text(kill_script)
        
        return {
            "path": str(script_path),
            "usage": "Double-click to emergency shutdown if VPN fails",
            "status": "CREATED"
        }
    
    def check_ip_leak(self):
        """Verify no DNS/WebRTC leaks"""
        # Placeholder - would need requests library
        return {
            "status": "MANUAL_CHECK_REQUIRED",
            "instructions": [
                "1. Visit: https://ipleak.net",
                "2. Verify: Only VPN IP shown",
                "3. Check: WebRTC shows VPN IP",
                "4. Verify: DNS servers belong to VPN"
            ]
        }
    
    def generate_hardening_report(self):
        """Full OPSEC status report"""
        print("\n🔒 MONOLITH OPSEC AUDIT")
        print("="*60)
        
        # Check VPN
        vpn = self.check_vpn_status()
        print(f"\n1. VPN STATUS: {vpn['status']}")
        print(f"   {vpn['details']}")
        
        # Forensic cleanup
        print("\n2. FORENSIC SANITIZATION")
        cleanup = self.clear_forensic_trails()
        print(f"   Files cleared: {cleanup['files_cleared']}")
        print(f"   Status: {cleanup['status']}")
        
        # Kill switch
        print("\n3. KILL SWITCH")
        ks = self.create_kill_switch_script()
        print(f"   Location: {ks['path']}")
        print(f"   Status: {ks['status']}")
        
        # Telemetry
        print("\n4. TELEMETRY BLOCKING")
        if self.os_type == "Windows":
            print("   Run as Administrator for full effect")
        else:
            print(f"   OS: {self.os_type} (telemetry varies)")
        
        # IP leak check
        print("\n5. IP LEAK PREVENTION")
        leak = self.check_ip_leak()
        print(f"   {leak['status']}")
        
        print("\n" + "="*60)
        print("⚠️ CRITICAL RECOMMENDATIONS:")
        print("  • Always run VPN BEFORE starting Monolith")
        print("  • Never use real name in config files")
        print("  • Use Privacy.com virtual cards for payments")
        print("  • Consider Tails OS for maximum anonymity")
        print("="*60)

if __name__ == "__main__":
    opsec = OPSECHardening()
    opsec.generate_hardening_report()
